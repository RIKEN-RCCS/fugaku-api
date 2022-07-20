from hpcrestapi.tests.common import check_popen_args
from hpcrestapi.tests.common import jwttoken
from hpcrestapi.tests.common import mock_popen
from hpcrestapi.tests.common import urandom
from hpcrestapi.system import sys_config
from hpcrestapi.main import app
from fastapi.testclient import TestClient
import os
import tempfile
from unittest import mock


client = TestClient(app)


##### FILE/DOWNLOAD ############################################################
def test_file_download():
    spec = {
        "system_type": "fugaku", # common code for slurm, torque

        "method": "post",
        "uri": "/file/download/relative%2Ffile%2Fpath",
        "expected_status_code": 200,
        "file_content": urandom(65536 * 32),

        "authorization": jwttoken(),

        "expected_popen_args": ["*/timeout", "250",
            "*/sudo", "-u", "nobody",
            "*/exec_syscall", "open", "./relative/file/path",
            str(0),
            str(0)],
        "communicate_return_value": (b"", b""),
        "returncode": 0,
    }
    download_test(spec)


def download_test(spec):
    p = mock_popen(spec["returncode"], spec["communicate_return_value"])

    with tempfile.TemporaryFile() as fp, \
         mock.patch("hpcrestapi.common.Popen", return_value=p) as m, \
         mock.patch("hpcrestapi.common.recv_fd", return_value=os.dup(fp.fileno())):
        sys_config.load_system_function(spec["system_type"])
        client.headers["Authorization"] = spec["authorization"]

        fp.write(spec["file_content"])
        fp.seek(0)

        response = client.get(spec["uri"])

        assert response.status_code == spec["expected_status_code"]
        assert response.content == spec["file_content"]
        a, = m.call_args_list[0][0]
        check_popen_args(a, spec["expected_popen_args"])
