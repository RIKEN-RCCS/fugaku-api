from hpcrestapi.tests.common import common_test
from hpcrestapi.tests.common import jwttoken
from hpcrestapi.main import app
from fastapi.testclient import TestClient
import os

client = TestClient(app)


##### FUGAKU JOBS/DELETE #######################################################
def test_job_delete_fugaku():
    spec = {
        "system_type": "fugaku",

        "method": "delete",
        "uri": "/jobs/6291500",
        "expected_status_code": 204,
        "expected_response_content": b"",

        "authorization": jwttoken(),

        "expected_popen_args": ["*/timeout", "250",
                       "*/sudo", "-u", "nobody",
                       "pjdel", "6291500"],
        "communicate_return_value": (
b"[INFO] PJM 0100 pjdel Accepted job 6291500.",
                b""),
        "returncode": 0,
    }
    common_test(client, spec)


##### SLURM JOBS/DELETE ########################################################
def test_job_delete_slurm():
    spec = {
        "system_type": "slurm",

        "method": "delete",
        "uri": "/jobs/92",
        "expected_status_code": 204,
        "expected_response_content": b"",

        "authorization": jwttoken(),

        "expected_popen_args": ["*/timeout", "250",
                       "*/sudo", "-u", "nobody",
                       "scancel", "92"],
        "communicate_return_value": (
b"",
                b""),
        "returncode": 0,
    }
    common_test(client, spec)


##### TORQUE JOBS/DELETE #######################################################
def test_job_delete_torque():
    spec = {
        "system_type": "torque",

        "method": "delete",
        "uri": "/jobs/94",
        "expected_status_code": 204,
        "expected_response_content": b"",

        "authorization": jwttoken(),

        "expected_popen_args": ["*/timeout", "250",
            "*/sudo", "-u", "nobody",
            "qdel", "94"],
        "communicate_return_value": (
b"",
                b""),
        "returncode": 0,
    }
    common_test(client, spec)
