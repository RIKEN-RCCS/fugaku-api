from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from hpcrestapi import common, config
from hpcrestapi.common import execute_command_argv
from hpcrestapi.common import redirect_exceptions_to_response
import logging
import pwd

router = APIRouter()

@router.get(
    "/hpc_system/groups/me",
    summary="Get Group Information"
)
async def hpc_system_group_info(user_id: str = Depends(common.get_authorized_user)):
    """# Get Group Information

## HPC_System/Groups/Me

The HPC_System/Groups/Me API allows a user to get the group information to which you belong.


## Endpoint

*get* /hpc_system/groups/me


## Parameters

None


## Default response example

```
Status: 200

{
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
  ]
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

Args:
    user_id      : string

Returns:
  - JSONResponse
    """
    return system_group(user_id)


@redirect_exceptions_to_response(422)
def system_group(user_id):
    logger = logging.getLogger(__name__)

    # groups コマンドで所属グループ一覧を取得
    command = ["/usr/bin/groups", user_id]
    retcode, outs, _ = execute_command_argv(user_id, command)
    if retcode == 0:
        # groupsコマンドの出力「ユーザ名 : 所属グループ名 ...」から
        # 所属グループ名のみを取り出し。
        group_name = outs.split(" : ")
        group_name = group_name[1].rstrip()
        group_name = group_name.split(' ')
    else:
        group_name = []

    item = {"group_name": group_name}

    logger.info(f"[{user_id}] - ret={retcode}")

    return JSONResponse(status_code=200, content=jsonable_encoder(item))
