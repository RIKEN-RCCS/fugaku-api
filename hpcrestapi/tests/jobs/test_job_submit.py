from hpcrestapi.tests.common import common_test
from hpcrestapi.tests.common import jwttoken
from hpcrestapi.main import app
from fastapi.testclient import TestClient
import os

client = TestClient(app)


post_body = {
    "jobfile": "/tmp/job1.sh",
    "qopt": "-v"
}


##### FUGAKU JOBS/SUBMIT #######################################################
def test_job_submit_fugaku():
    spec = {
        "system_type": "fugaku",

        "method": "post",
        "uri": "/jobs/",
        "post_body": post_body,
        "expected_status_code": 200,
        "expected_response_json": {"job_id": "6291500"},
        "expected_header": {"Location": "/jobs/6291500"},

        "authorization": jwttoken(),

        "expected_popen_args": ["*/timeout", "250",
                       "*/sudo", "-u", "nobody",
                       "*/exec_syscall", "submit",
                       "pjsub", "/tmp/job1.sh"],
        "communicate_return_value": (
b"""[INFO] PJM 0000 pjsub Job 6291500 submitted.
""",
                b""),
        "returncode": 0,
    }
    common_test(client, spec)


##### SLURM JOBS/SUBMIT ########################################################
def test_job_submit_slurm():
    spec = {
        "system_type": "slurm",

        "method": "post",
        "uri": "/jobs/",
        "post_body": post_body,
        "expected_status_code": 200,
        "expected_response_json": {"job_id": "92"},
        "expected_header": {"Location": "/jobs/92"},

        "authorization": jwttoken(),

        "expected_popen_args": ["*/timeout", "250",
                       "*/sudo", "-u", "nobody",
                       "*/exec_syscall", "submit",
                       "sbatch", "/tmp/job1.sh"],
        "communicate_return_value": (
b"""Submitted batch job 92
""",
                b""),
        "returncode": 0,
    }
    common_test(client, spec)


##### TORQUE JOBS/SUBMIT #######################################################
def test_job_submit_torque():
    spec = {
        "system_type": "torque",

        "method": "post",
        "uri": "/jobs/",
        "post_body": post_body,
        "expected_status_code": 200,
        "expected_response_json": {"job_id": "92"},
        "expected_header": {"Location": "/jobs/92"},

        "authorization": jwttoken(),

        "expected_popen_args": ["*/timeout", "250",
            "*/sudo", "-u", "nobody",
            "*/exec_syscall", "submit",
            "qsub", "/tmp/job1.sh"],
        "communicate_return_value": (
b"""92
""",
                b""),
        "returncode": 0,
    }
    common_test(client, spec)
