from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from hpcrestapi.common import get_authorized_user
from hpcrestapi.common import open_file_with_sudo
from hpcrestapi.common import realpath
from hpcrestapi.common import redirect_exceptions_to_response
import os

router = APIRouter()

@router.get(
    "/file/download/{file_path:path}",
    summary="Download a File",
    response_description="file body as a HTTP stream (chunk response)",
)
async def file_download(file_path: str,
        user_id: str = Depends(get_authorized_user)):
    """# Download a File

## File/Download

The File/Download API allows an user to download a file.
On successful operation, File content shall sent as HTTP
chunk response.

This API is available for authenticated users.


## Endpoint

*put* /file/download/{path}


## Parameters

None


## Default response example

```
Status: 200
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

*hpcrestapi.file.file_download.download*

Args:
    file_path    : string
    user_id      : string

Returns:
  - StreamingResponse
"""
    return download(user_id, file_path)


@redirect_exceptions_to_response(404)
def download(user_id, file_path):
    d = open_file_with_sudo(user_id, realpath(file_path), os.O_RDONLY, 0)
    f = os.fdopen(d, "br")
    return StreamingResponse(f)
