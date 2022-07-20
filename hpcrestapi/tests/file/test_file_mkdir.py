from hpcrestapi.tests.common import common_test
from hpcrestapi.tests.common import jwttoken
from hpcrestapi.main import app
from fastapi.testclient import TestClient
import os

client = TestClient(app)


##### FILE/MKDIR ###############################################################
def test_file_mkdir():
    spec = {
        "system_type": "fugaku", # don't care

        "method": "put",
        "uri": "/file/mkdir/tmp%2Fxyzzy?mode=750",
        "expected_status_code": 204,
        "expected_response_content": b"",

        "authorization": jwttoken(),

        "expected_popen_args": ["*/timeout", "250",
            "*/sudo", "-u", "nobody",
            "*/exec_syscall", "mkdir", "./tmp/xyzzy", "750"],
        "communicate_return_value": (
b"",
                b""),
        "returncode": 0,
    }
    common_test(client, spec)
