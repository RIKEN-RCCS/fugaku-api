from fastapi import APIRouter, Depends, Request
from fastapi import HTTPException
from starlette.responses import Response
from hpcrestapi.common import get_authorized_user
from hpcrestapi.common import open_file_with_sudo
from hpcrestapi.common import realpath
from hpcrestapi.common import redirect_exceptions_to_response
import logging
import os


router = APIRouter()


@router.post(
    "/file/upload/{file_path:path}",
    summary="Upload a File",
)
async def file_upload(file_path: str,
        request: Request,
        #file: UploadFile = File(...),
        user_id: str = Depends(get_authorized_user)):
    """# Upload a File

## File/Upload

The File/Upload API allows an user to upload a file.
File will be created with mode 0o600.

This API is available for authenticated users.


## Endpoint

*post* /file/upload/{path}


## Parameters

None


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

*hpcrestapi.file.file_upload*

Args:
    file_path    : string
    user_id      : string

Returns:
  - Response

"""
    try:
        d = open_file_with_sudo(user_id, realpath(file_path), os.O_RDWR|os.O_CREAT, 0o600)
        with os.fdopen(d, mode="wb") as f:
            async for chunk in request.stream():
                f.write(chunk)
        return Response(status_code=204)
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception(f"EXCEPTION {e.args}")
        if type(e.args) == tuple:
            message, = e.args
        else:
            message = e.args
        item = {"message": message, "type": "General System Error"}
        return JSONResponse(status_code=404,
                            content=jsonable_encoder(message))
