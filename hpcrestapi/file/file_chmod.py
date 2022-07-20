from fastapi import APIRouter, Depends
from starlette.responses import Response
from hpcrestapi.common import get_authorized_user
from hpcrestapi.common import chmod_with_sudo
from hpcrestapi.common import realpath
from hpcrestapi.common import redirect_exceptions_to_response

router = APIRouter()

@router.put(
    "/file/chmod/{file_path:path}",
    summary="change file modes",
    response_description="JSON",
)
async def file_chmod(file_path,
        mode,
        user_id: str = Depends(get_authorized_user)):
    """# Modify File Mode

## File/Chmod

The File/Chmod API modifies the file mode bits of the given
file as specified by mode parameter.
Modes should be absolute, that is an octal number, as
specified in POSIX.2 standard.

This API is available for authenticated users.


## Endpoint

*put* /file/chmod/{path}


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

*hpcrestapi.file.file_chmod.chmod*

Args:
    user_id      : string
    mode         : string
    file_path    : string

Returns:
  - JSONResponse
"""
    return chmod(user_id, mode, file_path)


@redirect_exceptions_to_response(404)
def chmod(user_id, mode, file_path):
    chmod_with_sudo(user_id, realpath(file_path), mode)
    return Response(status_code=204)
