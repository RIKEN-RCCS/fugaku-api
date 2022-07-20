from hpcrestapi.common import get_authorized_user
from hpcrestapi.common import redirect_exceptions_to_response
import hpcrestapi.system.sys_config as sys_config
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get(
    "/jobs/{jobid:int}",
    summary="Get Job Detail",
)
async def job_detail(jobid: int,
        user_id: str = Depends(get_authorized_user)):
    """# Get Job Detail

## Jobs/Dtail

The Jobs/Dtail API allows an user to view a running job's detail.

This API is available for authenticated users.


## Endpoint

*get* /jobs/{jobid}


## Parameters

None


## Default response example

```
Status: 200

{
  "job_id": "6291500",
  "job_name": "job1.sh",
  "status": "RNA",
  "user": "a03010",
  "group": "rccs-aot",
  "start_date": "2021-04-12T11:25:00",
  "elapse_time": "0000:00:00",
  "node_require": "12",
  "priority": "127",
  "accept": "2021-04-12T11:25:50",
  "queue": "small",
  "Fugaku:elapse_limit": "0000:01:00",
  "Fugaku:md": "NM",
  "Fugaku:vnode": "-",
  "Fugaku:core": "-",
  "Fugaku:v_mem": "-",
  "Fugaku:v_pol": "-",
  "Fugaku:e_pol": "-",
  "Fugaku:rank": "bychip",
  "Fugaku:lst": "QUE",
  "Fugaku:ec": "0",
  "Fugaku:pc": "0",
  "Fugaku:sn": "0",
  "Fugaku:reason": "-"
}
```

## Error response example

```
Status: 404

{
  "message": "Operation not permitted",
  "type": "OS Error"
}
```


# Implementation

*hpcrestapi.jobs.job_detail.job_detail*

Args:
    user_id  : string
    jobid    : string

Returns:
  - JSONResponse
"""
    return job_detail(user_id, jobid)


@redirect_exceptions_to_response(404)
def job_detail(user_id, jobid):
    return sys_config.system.job_detail(user_id, jobid)
