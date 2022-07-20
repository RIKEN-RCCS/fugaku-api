from hpcrestapi.tests.common import common_test
from hpcrestapi.tests.common import jwttoken
from hpcrestapi.main import app
from fastapi.testclient import TestClient
import os

client = TestClient(app)

class mockPwent():
    def __init__(self, pw_name, pw_passwd, pw_uid, pw_gid, pw_gecos, pw_dir, pw_shell):
        self.pw_name = pw_name
        self.pw_passwd = pw_passwd
        self.pw_uid = pw_uid
        self.pw_gid = pw_gid
        self.pw_gecos = pw_gecos
        self.pw_dir = pw_dir
        self.pw_shell = pw_shell


def test_hpc_users_common():
    spec = {
        "system_type": "fugaku", # common code for slurm, torque

        "method": "get",
        "uri": "/hpc_system/users/me",
        "expected_status_code": 200,
        "expected_response_json":
{"username": "nobody",
"uid": 1000,
"group_name": ["member","adm","cdrom","sudo","dip","plugdev","lpadmin","docker","wsgi"],
"gid": 200,
"home_directory": "/home/nobody",
"login_shell": "/bin/ksh"},

        "getpwnam_return_value": mockPwent("nobody", "*", 1000, 200, "Nobody", "/home/nobody", "/bin/ksh"),

        "authorization": jwttoken(),

        "expected_popen_args": ["*/timeout", "250",
            "*/sudo", "-u", "nobody",
            "*/groups", "nobody"],
        "communicate_return_value": (
b"""nobody : member adm cdrom sudo dip plugdev lpadmin docker wsgi
""",
            b""),
        "returncode": 0,
    }
    common_test(client, spec)
