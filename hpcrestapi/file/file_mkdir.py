from fastapi import APIRouter, Depends
from starlette.responses import Response
from hpcrestapi.common import get_authorized_user
from hpcrestapi.common import mkdir_with_sudo
from hpcrestapi.common import realpath
from hpcrestapi.common import redirect_exceptions_to_response
from typing import Optional

router = APIRouter()

@router.put(
    "/file/mkdir/{dir_path:path}",
    summary="Make a Directory",
    response_description="JSON",
)
async def file_mkdir(dir_path: str,
        mode: Optional[str] = "700",
        user_id: str = Depends(get_authorized_user)):
    """# Make a Directory

## File/Mkdir

The File/Mkdir API creates the directory as specified url,
with mode given as a parameter.
When mode parameter is omitted, 0o700 shall be used.

This API is available for authenticated users.


## Endpoint

*put* /file/mkdir/{path}


## Parameters

mode={mode}


## Default response example

```
Status: 204 No Content
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

*hpcrestapi.file.file_mkdir.mkdir*

Args:
    user_id     : string
    dir_path    : string
    mode        : string

Returns:
  - Response
"""
    return mkdir(user_id, dir_path, mode)


@redirect_exceptions_to_response(404)
def mkdir(user_id, dir_path, mode):
    mkdir_with_sudo(user_id, realpath(dir_path), mode)
    return Response(status_code=204)
