import asyncio
from hpcrestapi import config
from hpcrestapi.common import get_authorized_user
from hpcrestapi.common import set_x509_usermap
from hpcrestapi.tests.common import check_popen_args
from hpcrestapi.tests.common import common_test
from hpcrestapi.tests.common import jwttoken
from hpcrestapi.tests.common import mock_popen
from hpcrestapi.system import sys_config
from hpcrestapi.main import app
import base64
from fastapi.testclient import TestClient
import jwt
import time
import os
import tempfile
from unittest import mock
import common


client = TestClient(app)


class MyRequest():
    def __init__(self, headers):
        self.headers = headers


def gen_jwt_auth(sub, secret):
    iat = str(int(time.time()))
    jwtToken = jwt.encode({"sub":sub, "iat":iat}, secret, algorithm="HS256")
    return f"Bearer {jwtToken}"


def gen_basic_auth(sub, secret):
    basicToken = base64.b64encode(f"{sub}:{secret}".encode()).decode()
    return f"Basic {basicToken}"


def gen_ssl_auth(sub):
    return f"CN={sub},OU=benten,O=Benten,L=Shibuya,ST=Tokyo,C=JP"


def test_get_authorized_user_jwt():
    sub = "alice"
    secret = "random_secret"
    authorization = gen_jwt_auth(sub, secret)
    request = MyRequest({"authorization": authorization})
    expected = sub
    try:
        got = asyncio.run(get_authorized_user(request))
    except Exception as e:
        got = None
    assert expected == got


def test_get_authorized_user_basic():
    sub = "bob"
    secret = "random_secret"
    conf = config.settings.conf
    server_conf = conf["HPC_REST_API_SERVER"]
    ssl_client_s_dn = server_conf["ssl_client_s_dn"]
    authorization = gen_basic_auth(sub, secret)
    request = MyRequest({"authorization": authorization,
                         ssl_client_s_dn: "dummy-should-be-ignored"})
    expected = sub
    try:
        got = asyncio.run(get_authorized_user(request))
    except Exception as e:
        got = None
    assert expected == got


def test_get_authorized_user_ssl():
    set_x509_usermap(None)
    sub = "alice"
    conf = config.settings.conf
    server_conf = conf["HPC_REST_API_SERVER"]
    ssl_client_s_dn = server_conf["ssl_client_s_dn"]
    ssl_client_verify = server_conf["ssl_client_verify"]
    authorization = gen_ssl_auth(sub)
    request = MyRequest({ssl_client_s_dn: authorization,
                         ssl_client_verify: "SUCCESS"})
    expected = sub
    try:
        got = asyncio.run(get_authorized_user(request))
    except Exception as e:
        got = None
    assert expected == got


def test_get_authorized_user_ssl_d():
    d = {"alice": "bob"}
    set_x509_usermap(d)
    sub = "alice"
    conf = config.settings.conf
    server_conf = conf["HPC_REST_API_SERVER"]
    ssl_client_s_dn = server_conf["ssl_client_s_dn"]
    ssl_client_verify = server_conf["ssl_client_verify"]
    authorization = gen_ssl_auth(sub)
    request = MyRequest({ssl_client_s_dn: authorization,
                         ssl_client_verify: "SUCCESS"})
    expected = d.get(sub)
    try:
        got = asyncio.run(get_authorized_user(request))
    except Exception as e:
        got = None
    assert expected == got


def test_get_authorized_user_ssl_e():
    d = {"alice": "bob"}
    set_x509_usermap(d)
    sub = "charlie"
    conf = config.settings.conf
    server_conf = conf["HPC_REST_API_SERVER"]
    ssl_client_s_dn = server_conf["ssl_client_s_dn"]
    ssl_client_verify = server_conf["ssl_client_verify"]
    authorization = gen_ssl_auth(sub)
    request = MyRequest({ssl_client_s_dn: authorization,
                         ssl_client_verify: "SUCCESS"})
    expected = None
    try:
        got = asyncio.run(get_authorized_user(request))
    except Exception as e:
        got = None
    assert expected == got

