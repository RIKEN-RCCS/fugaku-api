from hpcrestapi.common import execute_command_argv
from hpcrestapi.common import MachineStatus
from hpcrestapi.common import normalize_date
from hpcrestapi.common import normalize_time
from hpcrestapi.common import parseToMachineStatus
from hpcrestapi.common import split_template
from hpcrestapi.common import submit_with_sudo
from hpcrestapi.common import system_status_with_sudo
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.responses import Response
import re
from starlette.responses import Response


def system_status(user_id):
    msg = system_status_with_sudo(user_id)
    item = {"message": msg}
    return JSONResponse(status_code=200, content=jsonable_encoder(item))


def job_detail(user_id, jobid):
    command = ["squeue", "--format=%all", "-j", str(jobid)]
    _, outs, _ = execute_command_argv(user_id, command)
    l = outs.split('\n')
    e = parseToJobStatus(l[1], l[0])
    if e is None:
        raise Exception(f"Parse entry failed: {e}")
    return JSONResponse(status_code=200, content=jsonable_encoder(e))


def job_submit(user_id, submit_job_request):
    outs = submit_with_sudo(user_id, submit_job_request.jobfile, "sbatch")
    r = re.match(".*Submitted batch job ([0-9][0-9]*).*", outs)
    jobid = r.group(1)
    headers = {"Location": f"/jobs/{jobid}"}
    item = {"job_id": f"{jobid}"}
    return JSONResponse(status_code=200, headers=headers,
                    content=jsonable_encoder(item))


def job_delete(user_id, jobid):
    command = ["scancel", str(jobid)]
    status, outs, _ = execute_command_argv(user_id, command)
    if status != 0:
        item = {"errorMessage": outs}
        return JSONResponse(status_code=404, content=jsonable_encoder(item))
    return Response(status_code=204)


def job_list(user_id):
    command = ["squeue", "--format=%all", "-u", user_id]
    _, outs, _ = execute_command_argv(user_id, command)
    l = outs.split('\n')
    item = [i for i in [parseToJobStatus(e, l[0]) for e in l[1:]]
               if i is not None]
    return JSONResponse(status_code=200, content=jsonable_encoder(item))


###################################################
##### UTILITIES
###################################################


def parseToJobStatus(e, tp):
    """
    parse squeue output
    """
    ts = tp.split('|')
    es = e.split('|')
    if len(ts) != len(es):
        return None
    v = zip(ts, es)
    v = dict(v)
    return {
        "job_id": v["JOBID"],
        "job_name": v["NAME"],
        "status": v["ST"],
        "user": v["USER"],
        "group": v["GROUP"],
        "elapse_time": normalize_time(v["TIME"]),
        "node_require": v["NODES"],
        "priority": v["PRIORITY"],
        "accept": normalize_date(v["SUBMIT_TIME"]),
        "queue": v["PARTITION"],
        "Slurm:ACCOUNT": v["ACCOUNT"],
        "Slurm:GRES": v["GRES"],
        "Slurm:MIN_CPUS": v["MIN_CPUS"],
        "Slurm:MIN_TMP_DISK": v["MIN_TMP_DISK"],
        "Slurm:END_TIME": v["END_TIME"],
        "Slurm:FEATURES": v["FEATURES"],
        "Slurm:OVER_SUBSCRIBE": v["OVER_SUBSCRIBE"],
        "Slurm:COMMENT": v["COMMENT"],
        "Slurm:TIME_LIMIT": v["TIME_LIMIT"],
        "Slurm:MIN_MEMORY": v["MIN_MEMORY"],
        "Slurm:REQ_NODES": v["REQ_NODES"],
        "Slurm:COMMAND": v["COMMAND"],
        "Slurm:QOS": v["QOS"],
        "Slurm:REASON": v["REASON"],
        "Slurm:RESERVATION": v["RESERVATION"],
        "Slurm:WCKEY": v["WCKEY"],
        "Slurm:EXC_NODES": v["EXC_NODES"],
        "Slurm:NICE": v["NICE"],
        "Slurm:S:C:T": v["S:C:T"],
        "Slurm:EXEC_HOST": v["EXEC_HOST"],
        "Slurm:CPUS": v["CPUS"],
        "Slurm:DEPENDENCY": v["DEPENDENCY"],
        "Slurm:ARRAY_JOB_ID": v["ARRAY_JOB_ID"],
        "Slurm:SOCKETS_PER_NODE": v["SOCKETS_PER_NODE"],
        "Slurm:CORES_PER_SOCKET": v["CORES_PER_SOCKET"],
        "Slurm:THREADS_PER_CORE": v["THREADS_PER_CORE"],
        "Slurm:ARRAY_TASK_ID": v["ARRAY_TASK_ID"],
        "Slurm:TIME_LEFT": v["TIME_LEFT"],
        "Slurm:NODELIST": v["NODELIST"],
        "Slurm:CONTIGUOUS": v["CONTIGUOUS"],
        "Slurm:NODELIST(REASON)": v["NODELIST(REASON)"],
        "Slurm:START_TIME": v["START_TIME"],
        "Slurm:STATE": v["STATE"],
        "Slurm:LICENSES": v["LICENSES"],
        "Slurm:CORE_SPEC": v["CORE_SPEC"],
        "Slurm:SCHEDNODES": v["SCHEDNODES"],
        "Slurm:WORK_DIR": v["WORK_DIR"]}
