from hpcrestapi.tests.common import common_test
from hpcrestapi.tests.common import jwttoken
from hpcrestapi.main import app
from fastapi.testclient import TestClient
import os

client = TestClient(app)


##### FILE/CHMOD ###############################################################
def test_file_chmod():
    spec = {
        "system_type": "fugaku", # don't care

        "method": "put",
        "uri": "/file/chmod/%2Ftmp%2Fxyzzy?mode=4755",
        "expected_status_code": 204,
        "expected_response_content": b"",

        "authorization": jwttoken(),

        "expected_popen_args": ["*/timeout", "250",
            "*/sudo", "-u", "nobody",
            "*/exec_syscall", "chmod", "/tmp/xyzzy", "4755"],
        "communicate_return_value": (
b"",
                b""),
        "returncode": 0,
    }
    common_test(client, spec)
