from hpcrestapi.common import execute_command_argv
from hpcrestapi.common import MachineStatus
from hpcrestapi.common import normalize_date
from hpcrestapi.common import parseToMachineStatus
from hpcrestapi.common import split_template
from hpcrestapi.common import submit_with_sudo
from hpcrestapi.common import system_status_with_sudo
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.responses import Response
from starlette.responses import Response


def system_status(user_id):
    msg = system_status_with_sudo(user_id)
    item = {"message": msg}
    return JSONResponse(status_code=200, content=jsonable_encoder(item))


def job_detail(user_id, jobid):
    command = ["qstat", "-f", str(jobid)]
    _, outs, _ = execute_command_argv(user_id, command)
    l = separateJobStatus(outs.split('\n'))
    e = parseToJobStatus(l[0])
    if e is None:
        raise Exception(f"Parse entry failed: {e}")
    return JSONResponse(status_code=200, content=jsonable_encoder(e))


def job_submit(user_id, submit_job_request):
    outs = submit_with_sudo(user_id, submit_job_request.jobfile, "qsub")
    r = outs.strip()
    jobid = r
    headers = {"Location": f"/jobs/{jobid}"}
    item = {"job_id": f"{jobid}"}
    return JSONResponse(status_code=200, headers=headers,
                    content=jsonable_encoder(item))


def job_delete(user_id, jobid):
    command = ["qdel", str(jobid)]
    status, outs, _ = execute_command_argv(user_id, command)
    if status != 0:
        item = {"errorMessage": outs}
        return JSONResponse(status_code=404, content=jsonable_encoder(item))
    return Response(status_code=204)


def job_list(user_id):
    command = ["qstat", "-f"]
    _, outs, _ = execute_command_argv(user_id, command)
    l = separateJobStatus(outs.split('\n'))
    item = [parseToJobStatus(e) for e in l]
    return JSONResponse(status_code=200, content=jsonable_encoder(item))


###################################################
##### UTILITIES
###################################################


def separateJobStatus(e):
    start_key = "Job Id:"
    r = list()
    item = list()
    for i in e:
        if i.startswith(start_key):
            if item != []:
                r.append(item)
                item = list()
            k, v = i.split(':')
            item.append((k.strip(), v.strip()))
        elif '=' in i:
            k, v = i.split('=')
            item.append((k.strip(), v.strip()))
        else:
            pass
    if item != []:
        r.append(item)
        item = list()
    return r


def parseToJobStatus(e):
    """
    parse qstat output
    """
    v = dict(e)
    return {
        "job_id": v["Job Id"],
        "job_name": v["Job_Name"],
        "status": v["job_state"],
        "user": v["euser"],
        "group": v["egroup"],
        "start_date": normalize_date(v["qtime"]),
        "priority": v["Priority"],
        "queue": v["queue"],
        "Torque:JobOwner": v["Job_Owner"],
        "Torque:Resource_List.walltime": v["Resource_List.walltime"],
        "Torque:Resource_List.nodect": v["Resource_List.nodect"],
        "Torque:Resource_List.ncpus": v["Resource_List.ncpus"]}
