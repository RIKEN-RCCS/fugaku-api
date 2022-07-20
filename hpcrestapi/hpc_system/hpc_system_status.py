from hpcrestapi.common import MachineStatus
from hpcrestapi.common import get_authorized_user
from hpcrestapi.common import redirect_exceptions_to_response
from hpcrestapi.system.sys_config import system
from fastapi import APIRouter, Depends
from typing import List


router = APIRouter()


@router.get(
    "/hpc_system/status",
    summary="Get System Status",
    response_model=List[MachineStatus]
)
async def hpc_system_status(user_id: str = Depends(get_authorized_user)):
    """# Get System Status

## HPC_System/Status

The HPC_System/Status API allows an user to submit a job.
This API is available for authenticated users.


## Endpoint

*put* /jobs/


## Parameters

None


## Default response example

```
Status: 200

{
  "message": "UP"
}
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


*hpcrestapi.hpc_system.hpc_system_status.system_status*

Args:
    user_id      : string

Returns:
  - JSONResponse
    """
    return system_status(user_id)


@redirect_exceptions_to_response(500)
def system_status(user_id):
    return system.system_status(user_id)
