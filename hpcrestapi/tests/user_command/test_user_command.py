from hpcrestapi.tests.common import common_test
from hpcrestapi.tests.common import jwttoken
from hpcrestapi.main import app
from fastapi.testclient import TestClient
import os

client = TestClient(app)


post_body = {
    "command": "uname -r"
}


##### USER_COMMAND/COMMAND #####################################################
def test_user_command():
    spec = {
        "system_type": "fugaku", # don't care

        "method": "post",
        "uri": "/command",
        "post_body": post_body,
        "expected_status_code": 200,
        "expected_response_json": {
  "retcode": 0,
  "stdout": "4.18.0-193.el8.x86_64\n",
  "stderr": ""
},

        "authorization": jwttoken(),

        "expected_popen_args": ["*/timeout", "250",
            "*/sudo", "-u", "nobody",
            "*/exec_syscall", "shell"],
        "expected_communicate_stdin": b"uname -r",

        "communicate_return_value": (
b"""4.18.0-193.el8.x86_64
""",
                b""),
        "returncode": 0,
    }
    common_test(client, spec)
