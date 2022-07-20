from hpcrestapi.tests.common import common_test
from hpcrestapi.tests.common import jwttoken
from hpcrestapi.main import app
from fastapi.testclient import TestClient
import os

client = TestClient(app)


##### FILE/LIST ################################################################
def test_file_list():
    spec = {
        "system_type": "fugaku", # don't care

        "method": "get",
        "uri": "/file/list/tmp%2fa%2Fb",
        "expected_status_code": 200,
        "expected_response_json":

[{"path": "bkt78", "st_mode": "drwxr-xr-x", "st_mtime": "2021-03-26T16:38:00"}, {"path": "foo", "st_mode": "-rwsrwxrwx", "st_mtime": "2021-03-17T17:37:50"}, {"path": "bkt5", "st_mode": "drwx------", "st_mtime": "2021-03-26T10:27:48"}, {"path": "bkt2", "st_mode": "drwx------", "st_mtime": "2021-03-26T11:37:47"}, {"path": "bkt6", "st_mode": "drwx------", "st_mtime": "2021-03-26T11:37:06"}, {"path": "bkt99", "st_mode": "drwxr-xr-x", "st_mtime": "2021-03-26T16:36:51"}, {"path": "bkt79", "st_mode": "drwx------", "st_mtime": "2021-03-26T16:37:47"}, {"path": "bar", "st_mode": "-rwx------", "st_mtime": "2021-03-24T11:21:04"}, {"path": "baz", "st_mode": "-rw-------", "st_mtime": "2021-04-15T12:06:01"}, {"path": "bkt7", "st_mode": "drwx------", "st_mtime": "2021-03-26T11:22:04"}, {"path": "bkt9", "st_mode": "drwx------", "st_mtime": "2021-03-25T10:33:09"}, {"path": "bkt8", "st_mode": "drwxr-xr-x", "st_mtime": "2021-03-25T10:33:27"}],

        "authorization": jwttoken(),

        "expected_popen_args": ["*/timeout", "250",
            "*/sudo", "-u", "nobody",
            "*/exec_syscall", "listdir", "./tmp/a/b"],
        "communicate_return_value": (
b"""[{"path": "bkt78", "st_mode": "drwxr-xr-x", "st_mtime": "2021-03-26T16:38:00"}, {"path": "foo", "st_mode": "-rwsrwxrwx", "st_mtime": "2021-03-17T17:37:50"}, {"path": "bkt5", "st_mode": "drwx------", "st_mtime": "2021-03-26T10:27:48"}, {"path": "bkt2", "st_mode": "drwx------", "st_mtime": "2021-03-26T11:37:47"}, {"path": "bkt6", "st_mode": "drwx------", "st_mtime": "2021-03-26T11:37:06"}, {"path": "bkt99", "st_mode": "drwxr-xr-x", "st_mtime": "2021-03-26T16:36:51"}, {"path": "bkt79", "st_mode": "drwx------", "st_mtime": "2021-03-26T16:37:47"}, {"path": "bar", "st_mode": "-rwx------", "st_mtime": "2021-03-24T11:21:04"}, {"path": "baz", "st_mode": "-rw-------", "st_mtime": "2021-04-15T12:06:01"}, {"path": "bkt7", "st_mode": "drwx------", "st_mtime": "2021-03-26T11:22:04"}, {"path": "bkt9", "st_mode": "drwx------", "st_mtime": "2021-03-25T10:33:09"}, {"path": "bkt8", "st_mode": "drwxr-xr-x", "st_mtime": "2021-03-25T10:33:27"}]
""",
                b""),
        "returncode": 0,
    }
    common_test(client, spec)
