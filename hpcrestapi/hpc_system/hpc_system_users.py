from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from hpcrestapi import common
from hpcrestapi.common import execute_command_argv
from hpcrestapi.common import redirect_exceptions_to_response
from pwd import getpwnam
import logging
import pwd


router = APIRouter()

@router.get(
    "/hpc_system/users/me",
    summary="Get User Information"
)
async def hpc_system_users(user_id: str = Depends(common.get_authorized_user)):
    """# Get User Information

## HPC_System/Users/Me

The HPC_System/Users/Me API allows a user to get a yourself information.


## Endpoint

*get* /hpc_system/users/me


## Parameters

None


## Default response example

```
Status: 200

{
  "username": "nobody",
  "uid": 1000,
  "group_name": [
    "member",
    "adm",
    "cdrom",
    "sudo",
    "dip",
    "plugdev",
    "lpadmin",
    "docker",
    "wsgi"
  ],
  "gid": 200,
  "home_directory": "/home/nobody",
  "login_shell": "/bin/ksh"
}
```


## Error response example

```
Status: 422

{
  "detail": [
    {
      "loc": [
        "header",
        "authorization"
      ],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```


# Implementation

*hpcrestapi.hpc_system.hpc_system_users*

Args:
    user_id      : string

Returns:

  - JSONResponse
    """
    return system_user(user_id)


@redirect_exceptions_to_response(422)
def system_user(user_id):
    logger = logging.getLogger(__name__)

    r = getpwnam(user_id)

    # groups コマンドで所属グループ一覧を取得
    command = ["/usr/bin/groups", user_id]
    retcode, outs, _ = execute_command_argv(user_id, command)
    if retcode == 0:
        # groupsコマンドの出力「ユーザ名 : 所属グループ名１ ...」から
        # 所属グループ名のみを取り出し。
        group_name = outs.split(" : ")
        group_name = group_name[1].rstrip()
        group_name = group_name.split(' ')
    else:
        group_name = []

    item = { "username": r.pw_name,
             "uid": r.pw_uid,
             "group_name": group_name,
             "gid": r.pw_gid,
             "home_directory": r.pw_dir,
             "login_shell": r.pw_shell
    }

    logger.info(f"[{user_id}] - ret={retcode}")

    return JSONResponse(status_code=200, content=jsonable_encoder(item))
