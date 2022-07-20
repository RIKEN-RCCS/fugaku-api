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
    command = ["pjstat", "-v", str(jobid)]
    _, outs, _ = execute_command_argv(user_id, command)
    l = outs.split('\n')
    e = parseToJobStatus(l[1], l[0])
    if e is None:
        raise Exception(f"Parse entry failed: {e}")
    return JSONResponse(status_code=200, content=jsonable_encoder(e))


def job_submit(user_id, submit_job_request):
    outs = submit_with_sudo(user_id, submit_job_request.jobfile, "pjsub")
    r = re.match(".*pjsub Job ([0-9][0-9]*) submitted.*", outs)
    jobid = r.group(1)
    headers = {"Location": f"/jobs/{jobid}"}
    item = {"job_id": f"{jobid}"}
    return JSONResponse(status_code=200, headers=headers,
                    content=jsonable_encoder(item))


def job_delete(user_id, jobid):
    command = ["pjdel", str(jobid)]
    status, outs, _ = execute_command_argv(user_id, command)
    if status != 0:
        item = {"errorMessage": outs}
        return JSONResponse(status_code=404, content=jsonable_encoder(item))
    return Response(status_code=204)


def job_list(user_id):
    command = ["pjstat", "-v"]
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
    parse pjstat output
    """
    u = split_template(tp)
    v = [(tp[start:end].strip(), e[start:end].strip()) for (start, end) in u]
    v = dict(v)
    if v["JOB_ID"] == "":
        return None
    return {
        "job_id": v["JOB_ID"],
        "job_name": v["JOB_NAME"],
        "status": v["ST"],
        "user": v["USER"],
        "group": v["GROUP"],
        "start_date": normalize_date(v["START_DATE"]),
        "elapse_time": normalize_time(v["ELAPSE_TIM"]),
        "node_require": v["NODE_REQUIRE"],
        "priority": v["PRI"],
        "accept": normalize_date(v["ACCEPT"]),
        "queue": v["RSC_GRP"],
        "Fugaku:elapse_limit": normalize_time(v["ELAPSE_LIM"]),
        "Fugaku:md": v["MD"],
        "Fugaku:vnode": v["VNODE"],
        "Fugaku:core": v["CORE"],
        "Fugaku:v_mem": v["V_MEM"],
        "Fugaku:v_pol": v["V_POL"],
        "Fugaku:e_pol": v["E_POL"],
        "Fugaku:rank": v["RANK"],
        "Fugaku:lst": v["LST"],
        "Fugaku:ec": v["EC"],
        "Fugaku:pc": v["PC"],
        "Fugaku:sn": v["SN"],
        "Fugaku:reason": v["REASON"]}
