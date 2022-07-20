from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from hpcrestapi.common import get_authorized_user
from hpcrestapi.common import listdir_with_sudo
from hpcrestapi.common import realpath
from hpcrestapi.common import redirect_exceptions_to_response
import json

router = APIRouter()

@router.get(
    "/file/list/{file_path:path}",
    summary="List Directory",
)
async def file_list(file_path: str,
        user_id: str = Depends(get_authorized_user)):
    """# List Directory

## File/List

The File/List API displays directory content as specified.

This API is available for authenticated users.


## Endpoint

*get* /file/list/{path}


## Parameters

None


## Default response example

```
Status: 200

[
  {
    "path": "bkt78",
    "st_mode": "drwxr-xr-x",
    "st_mtime": "2021-03-26T16:38:00"
  },
  {
    "path": "foo",
    "st_mode": "-rwsrwxrwx",
    "st_mtime": "2021-03-17T17:37:50"
  },
  {
    "path": "bkt5",
    "st_mode": "drwx------",
    "st_mtime": "2021-03-26T10:27:48"
  }
]
```


## Error response example

```
Status: 404

{
  "message": "Not a directory",
  "type": "OS Error"
}
```


# Implementation

*hpcrestapi.file.file_list.listdir*

Args:
    file_path    : string
    user_id      : string

Returns:
  - JSONResponse
"""
    return listdir(user_id, file_path)


@redirect_exceptions_to_response(404)
def listdir(user_id, file_path):
    s = listdir_with_sudo(user_id, realpath(file_path))
    return JSONResponse(status_code=200, content=json.loads(s))
