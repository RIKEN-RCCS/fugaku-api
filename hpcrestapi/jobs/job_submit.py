from hpcrestapi.common import SubmitJobRequest
from hpcrestapi.common import get_authorized_user
from hpcrestapi.common import redirect_exceptions_to_response
import hpcrestapi.system.sys_config as sys_config
from fastapi import APIRouter, Depends

router = APIRouter()

@router.post(
    "/jobs/",
    summary="Submit a Job",
)
async def job_submit(request: SubmitJobRequest,
        user_id: str = Depends(get_authorized_user)):
    """# Submit a Job

## Jobs/Submit

The Jobs/Submit API allows an user to submit a job.
Post body consitsts as following:

```
{
"jobfile": "/tmp/job1.sh",
"qopt": "-v"
}
```

Job script file is given by 'jobfile'.
'qopt' is reserved for future extension.

On Successful job commitment, Jobs/Submit returns job resource by
'Location' header.

This API is available for authenticated users.


## Endpoint

*put* /jobs/


## Parameters

None


## Default response example

```
Status: 200
Location: /jobs/12543

{
  "job_id": "6291500"
}
```


## Error response example

```
Status: 400

{
  "message": "-",
  "type": "General Exception"
}
```


# Implementation


*hpcrestapi.jobs.job_submit.job_submit*

Args:
    request      : SubmitJobRequest
    user_id      : string

Returns:
  - JSONResponse
"""
    return job_submit(user_id, request)


@redirect_exceptions_to_response(400)
def job_submit(user_id, request):
    return sys_config.system.job_submit(user_id, request)
