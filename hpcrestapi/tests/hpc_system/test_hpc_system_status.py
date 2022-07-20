from hpcrestapi.tests.common import common_test
from hpcrestapi.tests.common import jwttoken
from hpcrestapi.main import app
from fastapi.testclient import TestClient
import os

client = TestClient(app)


def test_hpc_system_status_common():
    spec = {
        "system_type": "fugaku", # common code for slurm, torque

        "method": "get",
        "uri": "/hpc_system/status",
        "expected_status_code": 200,
        "expected_response_json": {"message": "UP"},

        "authorization": jwttoken(),

        "expected_popen_args": ["*/timeout", "250",
            "*/sudo", "-u", "nobody",
            "*/exec_syscall", "system_status"],
        "communicate_return_value": (b"UP", b""),
        "returncode": 0,
    }
    common_test(client, spec)
