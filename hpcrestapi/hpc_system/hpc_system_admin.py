from fastapi import APIRouter, Depends, HTTPException
from hpcrestapi.common import get_authorized_user
from hpcrestapi.common import execute_shell_script
from hpcrestapi.common import Command
from hpcrestapi.common import WebapiError
from hpcrestapi import config
import logging


logger = logging.getLogger("__name__")

router = APIRouter()


@router.post(
    "/hpc_system/admin/command-sample-post",
    summary="Execute a command - Sample",
)
async def run_command(command: Command,
                      user_id: str = Depends(get_authorized_user)):
    """# Execute a command - Sample

## HPC_System/Admin/Command-sample-post

The Execute API allows an user to execute a command.
Post body consists as following:

```
{
"command": "uname -r"
}
```


## Endpoint

*put* /command/


## Parameters

None


## Default response example

```
Status: 200

{
   "retcode": 0,
   "stdout": "3.10.0-1160.21.1.el7.x86_64",
   "stderr": ""
}
```


## Error response example

```
Status: 422

{
  "detail": [
    {
      "loc": [
        "string"
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```


# Implementation

*hpcrestapi.hpc_system.hpc_system_admin*

Args:

    command      : Command
    user_id      : string

Returns:

  - JSONResponse
    """
    logger = logging.getLogger(__name__)

    conf = config.settings.conf

    server_conf = conf["HPC_REST_API_SERVER"]
    api_conf = conf["HPC_REST_API"]

    cmd = command.command

    try:
        retcode, stdout, stderr = execute_shell_script(user_id, cmd)
    except Exception as e:
        logger.exception(f"EXCEPTION {e.args}")
        raise HTTPException(status_code=500, detail="System Error")

    logger.info(f"[{user_id}] - ret={retcode}")
    logger.debug(f"[{user_id}] - ret={retcode}, cmd=\"{command}\", stdout={stdout}, stderr={stderr}\n")
    return {"retcode": retcode, "stdout": stdout, "stderr": stderr}


@router.get(
    "/hpc_system/admin/command-sample-get",
    summary="Execute a command - Sample"
)
async def run_command(command: Command,
                      user_id: str = Depends(get_authorized_user)):
    """
    管理者指定コマンドを実行
    """

@router.head(
    "/hpc_system/admin/command-sample-head",
    summary="Execute a command - Sample"
)
async def run_command(command: Command,
                      user_id: str = Depends(get_authorized_user)):
    """
    管理者指定コマンドを実行
    """

@router.put(
    "/hpc_system/admin/command-sample-put",
    summary="Execute a command - Sample"
)
async def run_command(command: Command,
                      user_id: str = Depends(get_authorized_user)):
    """
    管理者指定コマンドを実行
    """

@router.delete(
    "/hpc_system/admin/command-sample-delete",
    summary="Execute a command - Sample"
)
async def run_command(command: Command,
                      user_id: str = Depends(get_authorized_user)):
    """
    管理者指定コマンドを実行
    """
# AttributeError: 'FastAPI' object has no attribute 'connect'
#@app.connect('/hpc_system/admin/command')
#async def execute_hpc_system_admin_command(admin_command: Command):
#    '''
#    管理者指定コマンドを実行
#    '''

@router.options(
    "/hpc_system/admin/command-sample-options",
    summary="Execute a command - Sample"
)
async def run_command(command: Command,
                      user_id: str = Depends(get_authorized_user)):
    """
    管理者指定コマンドを実行
    """

@router.trace(
    "/hpc_system/admin/command-sample-trace",
    summary="Execute a command - Sample"
)
async def run_command(command: Command,
                      user_id: str = Depends(get_authorized_user)):
    """
    管理者指定コマンドを実行
    """

@router.patch(
    "/hpc_system/admin/command-sample-patch",
    summary="Execute a command - Sample"
)
async def run_command(command: Command,
                      user_id: str = Depends(get_authorized_user)):
    """
    管理者指定コマンドを実行
    """
