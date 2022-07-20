from hpcrestapi.common import get_authorized_user
from hpcrestapi.common import redirect_exceptions_to_response
import hpcrestapi.system.sys_config as sys_config
from fastapi import APIRouter, Depends

router = APIRouter()

@router.delete(
    "/jobs/{jobid:int}",
    summary="Cancel a Job",
)
async def job_delete(jobid: int,
        user_id: str = Depends(get_authorized_user)):
    """# Cancel a Job

## Jobs/Cancel

The Jobs/Cancel API allows an user to cancel a running job.

This API is available for authenticated users.


## Endpoint

*delete* /jobs/{jobid}


## Parameters

None


## Default response example

```
Status: 204
```


## Error response example

```
Status: 404

{
  "message": "Operation not permitted",
  "type": "General Exception"
}
```


# Implementation

*hpcrestapi.jobs.job_cancel.job_delete*

Args:
    user_id  : string
    jobid    : string

Returns:
  - JSONResponse
"""
    return job_delete(user_id, jobid)


@redirect_exceptions_to_response(404)
def job_delete(user_id, jobid):
    return sys_config.system.job_delete(user_id, jobid)
