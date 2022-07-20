from hpcrestapi import config
from hpcrestapi.system import sys_config
import jwt
from unittest import mock
import os
import time
import sys


def myAssertEqual(got, expected):
    if not (got == expected):
        sys.stderr.write(f"@@@ got = {got}\n")
        sys.stderr.write(f"@@@ expected = {expected}\n")
    assert got == expected


def myAssertTrue(b, got, expected):
    if not (b):
        sys.stderr.write(f"@@@ got = {got}\n")
        sys.stderr.write(f"@@@ expected = {expected}\n")
    assert b


def jwttoken():
    sub = "nobody"
    secret = "secret"
    iat = str(int(time.time()))
    return ("Bearer " +
            jwt.encode({"sub": sub, "iat": iat}, secret, algorithm="HS256"))


def check_popen_args(got, expected):
    myAssertEqual(len(got), len(expected))
    for (g, e) in zip(got, expected):
        if e.startswith("*"):
            myAssertTrue(g.endswith(e[1:]), g, e)
        else:
            myAssertEqual(g, e)


def mock_popen(returncode, return_value):
    p = mock.MagicMock()
    p.communicate = mock.MagicMock()
    p.communicate.return_value = return_value
    p.returncode = returncode
    p.__enter__ = mock.Mock(return_value=p)
    p.__exit__ = mock.Mock(return_value=False)
    return p


def urandom(len):
    return os.urandom(32)


def common_test(client, spec):
    p = mock_popen(spec["returncode"], spec["communicate_return_value"])

    getpwnam_return_value = spec.get("getpwnam_return_value")

    with mock.patch("hpcrestapi.common.Popen", return_value=p) as m, \
         mock.patch("hpcrestapi.hpc_system.hpc_system_users.getpwnam",
                    return_value=getpwnam_return_value) as mockGetpwnam:

        sys_config.load_system_function(spec["system_type"])
        conf = config.settings.conf
        server_conf = conf['HPC_REST_API_SERVER']
        sudo_conf = server_conf['sudo']
        sudo_conf['sudo_path'] = "/usr/bin/sudo"
        client.headers["Authorization"] = spec["authorization"]
        method = spec["method"]
        uri = spec["uri"]
        if method == "get":
            response = client.get(uri)
        elif method == "post":
            response = client.post(uri, json=spec["post_body"])
        elif method == "put":
            response = client.put(uri)
        elif method == "delete":
            response = client.delete(uri)
        else:
            raise Exception("configuration error")
        if getpwnam_return_value is not None:
            mockGetpwnam.assert_any_call("nobody")
        expected_status_code = spec["expected_status_code"]
        myAssertEqual(response.status_code, expected_status_code)
        expected_response_json = spec.get("expected_response_json")
        expected_response_content = spec.get("expected_response_content")
        if expected_response_json is not None:
            myAssertEqual(response.json(), expected_response_json)
        elif expected_response_content is not None:
            myAssertEqual(response.content, expected_response_content)
        else:
            myAssertEqual(response.content, None)
        got, = m.call_args_list[0][0]
        check_popen_args(got, spec["expected_popen_args"])
        expected_communicate_stdin = spec.get("expected_communicate_stdin")
        if expected_communicate_stdin is not None:
            p.communicate.assert_any_call(expected_communicate_stdin)
