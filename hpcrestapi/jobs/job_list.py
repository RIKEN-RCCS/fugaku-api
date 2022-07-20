from hpcrestapi.common import get_authorized_user
from hpcrestapi.common import redirect_exceptions_to_response
import hpcrestapi.system.sys_config as sys_config
from fastapi import APIRouter, Depends
from typing import List

router = APIRouter()

@router.get(
    "/jobs/",
    summary="Get Job List",
)
async def job_list(
        user_id: str = Depends(get_authorized_user)):
    """# Get a JobList

## Jobs/List

The Jobs/List API allows an user to get a list of
jobs that is still running.

This API is available for authenticated users.


## Endpoint

*get* /jobs/


## Parameters

None


## Default response example

```
Status: 200

[
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
  },
  {
    "job_id": "6291501",
    "job_name": "job1.sh",
    "status": "RNA",
    "user": "a03010",
    "group": "rccs-aot",
    "start_date": "2021-04-12T11:25:00",
    "elapse_time": "0000:00:00",
    "node_require": "12",
    "priority": "127",
    "accept": "2021-04-12T11:25:51",
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
]
```

## Error response example

```
Status: 500

{
  "message": "-",
  "type": "General Exception"
}
```


# Implementation

*hpcrestapi.jobs.job_list.job_list*

Args:
    user_id      : string

Returns:
  - JSONResponse
"""
    return job_list(user_id)


@redirect_exceptions_to_response(500)
def job_list(user_id):
    return sys_config.system.job_list(user_id)
