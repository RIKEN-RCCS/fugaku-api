from hpcrestapi import config
import array
import base64
from fastapi import HTTPException, status
from fastapi import Header
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from functools import reduce
import json
import jwt
import logging
import os
import re
from pydantic import BaseModel
import socket
from subprocess import Popen, PIPE, TimeoutExpired
import tempfile
import time
from typing import List


"""共通項を格納

Todo:
    * 各クラス・メソッドの再構成

"""

class WebapiError(BaseModel):
    """Portalエラー
    * err_msg: エラーメッセージ（本文）
    * status: 'NG'のみ
    * err_id: 形式:EXYYNNN
    *               X: 0.ユーザ向け 1.CMS向け
    *               YY: 機能ID
    *               NNN: 機能内連番
    * error: エラーメッセージ（件名）
    """
    err_msg: str = ''
    status: str = 'NG'
    err_id: str = ''
    error: str = ''


def abspath(filename):
    """webapiフォルダからの相対パスを絶対パスに変換する
    """
    routers_dir = os.path.dirname(os.path.abspath(__file__))
    top_dir = os.path.abspath(f"{routers_dir}/../../")
    return f"{top_dir}/{filename}"


def redirect_exceptions_to_response(code):

    def redirect_exceptions_to_response_modifier(fn):
        def newfn(*args):
            logger = logging.getLogger(__name__)
            try:
                return fn(*args)
            except OSError as e:
                logger.exception(f"EXCEPTION {e.args}")
                errno, message = e.args
                item = {"message": message, "type": "OS Error"}
                return JSONResponse(status_code=code,
                                    content=jsonable_encoder(item))
            except HTTPException as e:
                item = {"message": e.detail, "type": "API Error"}
                return JSONResponse(status_code=code,
                                    content=jsonable_encoder(item))
                raise e
            except Exception as e:
                logger.exception(f"EXCEPTION {e.args}")
                if type(e.args) == tuple:
                    message, = e.args
                else:
                    message = e.args
                item = {"message": message, "type": "General System Error"}
                return JSONResponse(status_code=code,
                                    content=jsonable_encoder(message))
        return newfn

    return redirect_exceptions_to_response_modifier


def complete_path(basename):
    pkgdir = os.path.normpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return os.path.normpath(os.path.join(pkgdir, "..", basename))


def popen_command_argv_with_sudo(user_id, user_command, stdout=PIPE,
        nochidir=False):
    conf = config.settings.conf
    server_conf = conf['HPC_REST_API_SERVER']
    sudo_conf = server_conf['sudo']
    timeout_path = sudo_conf['timeout_path']
    timeout = sudo_conf['exec_cmd_timeout']
    sudo_path = sudo_conf['sudo_path']
    chdir = {}
    if not nochidir:
        chdir = {"cwd": "/"}

    timeout_cmd = [timeout_path, str(timeout)]
    sudo_cmd = ([sudo_path, "-u", user_id] if sudo_path != "" else ["env"])
    #user_environ = [f"PYTHONPATH={PYTHONPATH}"]
    sudo_environ = os.environ
    #cmd = (timeout_cmd + sudo_cmd + user_environ + user_command)
    cmd = (timeout_cmd + sudo_cmd + user_command)
    return Popen(cmd, stdin=PIPE, stdout=stdout, stderr=PIPE,
                 env=sudo_environ, **chdir)


def execute_command_argv(user_id, user_command):
    logger = logging.getLogger(__name__)
    outs, errs = None, None
    with popen_command_argv_with_sudo(user_id, user_command) as proc:
        try:
            outs, errs = proc.communicate()
            if proc.returncode == 124: # killed on timeout
                logger.exception(f"EXCEPTION TIMEOUT")
                raise TimeoutExpired(
                    cmd=user_command, timeout=timeout, output=result)
            if proc.returncode != 0:
                logger.warning(f"RETCODE {user_command} return {proc.returncode}")
        except Exception as e:
            logger.exception(f"EXCEPTION {e.args}")
            raise e
        return (proc.returncode, outs.decode(), errs.decode())


def syscall_popen(user_id, fn, argv, stdout=PIPE):
    conf = config.settings.conf
    server_conf = conf['HPC_REST_API_SERVER']
    sudo_conf = server_conf['sudo']
    cmd_basename = sudo_conf['exec_syscall_path']
    exec_syscall = complete_path(cmd_basename)
    cmd = [exec_syscall, fn] + argv
    return popen_command_argv_with_sudo(user_id, cmd, stdout=stdout)


def check_sycall_errs(returncode, errs):
    if returncode == 0:
        return
    j = None
    try:
        j = json.loads(errs)
    except:
        pass
    if (j is not None and len(j) == 2 and
        type(j[0]) == int and type(j[1]) == str):
        raise OSError(j[0], j[1])
    # always raise exception here
    raise Exception(f"general exception: {errs}")


def open_file_with_sudo(user_id, path, flags, mode):
    sv0, sv1 = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM, 0)
    try:
        sv1.set_inheritable(True)
        with syscall_popen(user_id, "open",
                [path, str(flags), str(mode)], stdout=sv1) as proc:
            d = recv_fd(sv0)  # may raise OSError
            proc.wait()       # `open' never fail
    finally:
        sv0.close()
        sv1.close()
    return d


def recv_fd(sock):
    msglen = 48               # is enough
    fds = array.array("i")
    errnos = array.array("i")
    anclen = socket.CMSG_LEN(fds.itemsize)
    msg, ancdata, flags, addr = sock.recvmsg(msglen, anclen)
    for cmsg_level, cmsg_type, cmsg_data in ancdata:
        if cmsg_level == socket.SOL_SOCKET and cmsg_type == socket.SCM_RIGHTS:
            l = len(cmsg_data)
            e = l - (l % fds.itemsize)
            fds.frombytes(cmsg_data[:e])
    errnos.frombytes(msg)
    errno = list(errnos)[0]
    if errno != 0:
        raise OSError(errno, os.strerror(errno))
    return list(fds)[0]


def listdir_with_sudo(user_id, path):
    with syscall_popen(user_id, "listdir", [path]) as proc:
        outs, errs = proc.communicate()
        proc.wait()
        check_sycall_errs(proc.returncode, errs.decode())
        return outs.decode()


def chmod_with_sudo(user_id, path, mode):
    with syscall_popen(user_id, "chmod", [path, mode]) as proc:
        outs, errs = proc.communicate()
        proc.wait()
        check_sycall_errs(proc.returncode, errs.decode())
        return 0


def mkdir_with_sudo(user_id, path, mode):
    with syscall_popen(user_id, "mkdir", [path, mode]) as proc:
        outs, errs = proc.communicate()
        proc.wait()
        check_sycall_errs(proc.returncode, errs.decode())
        return 0


def system_status_with_sudo(user_id):
    with syscall_popen(user_id, "system_status", []) as proc:
        outs, errs = proc.communicate()
        proc.wait()
        check_sycall_errs(proc.returncode, errs.decode())
        return outs.decode()


def submit_with_sudo(user_id, script, sub_command):
    with syscall_popen(user_id, "submit", [sub_command, script]) as proc:
        outs, errs = proc.communicate()
        proc.wait()
        check_sycall_errs(proc.returncode, errs.decode())
        return outs.decode()


def execute_shell_script(user_id, user_command):
    logger = logging.getLogger(__name__)
    conf = config.settings.conf
    server_conf = conf['HPC_REST_API_SERVER']
    sudo_conf = server_conf['sudo']
    timeout = sudo_conf['exec_cmd_timeout']

    with syscall_popen(user_id, "shell", []) as proc:
        outs, errs = None, None
        try:
            outs, errs = proc.communicate(user_command.encode("utf-8"))

            if proc.returncode == 124: # killed on timeout
                logger.exception(f"EXCEPTION TIMEOUT")
                raise TimeoutExpired(
                    cmd=user_command, timeout=timeout, output=result)

            if proc.returncode != 0:
                logger.warning(f"RETCODE 'syscall_popen' return {proc.returncode}")

        except Exception as e:
            logger.exception(f"EXCEPTION {e.args}")
            raise e

        return (proc.returncode, outs.decode(), errs.decode())


async def get_authorized_user(request: Request):
    conf = config.settings.conf
    server_conf = conf["HPC_REST_API_SERVER"]
    ssl_client_s_dn = server_conf["ssl_client_s_dn"]
    ssl_client_verify = server_conf["ssl_client_verify"]
    ssl_s_dn = None
    if request.headers.get(ssl_client_verify, None) == "SUCCESS":
        ssl_s_dn = request.headers.get(ssl_client_s_dn, None)
    authorization = request.headers.get("authorization", None)
    logger = logging.getLogger("app")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        #headers={"WWW-Authenticate": "Bearer"},
    )
    authtype = None
    token = None
    if authorization is not None:
        tmp = authorization.split(' ')
        authtype = tmp[0] if len(tmp) == 2 else None
        try:
            token = tmp[1]
        except:
            pass
    user_id = None
    try:
        if authtype == "Basic" and token is not None:
            user_id = extract_userid_from_basic_token(token)
        elif authtype == "Bearer" and token is not None:
            user_id = extract_userid_from_bearer_token(token)
        elif ssl_s_dn is not None:
            user_id = get_userid_from_s_dn(ssl_s_dn)
        else:
            raise credentials_exception
    except:
        raise credentials_exception
    if user_id is None:
        raise credentials_exception
    return user_id


def extract_userid_from_bearer_token(encoded_token):
    jwt_token = None
    try:
        # We do not verify JWT token here, as the token is verified by
        # http server.
        jwt_token = jwt.decode(encoded_token,
                               options={"verify_signature": False},
                               algorithms=["HS256"])
        # keycloak 経由の場合はname, auth-api経由はsub
        if jwt_token.get("aud") == "account":
            name = jwt_token.get("name")
        else:
            name = jwt_token.get("sub")

    except Exception as e:
        logger.warning(f"jwt decode error.{e.args}")
        raise Exception

    return name


def extract_userid_from_basic_token(encoded_token):
    token = base64.b64decode(encoded_token).decode()
    l = token.split(":")
    if len(l) != 2:
        raise Exception
    return str(l[0])


def split_template(template, right_justified=False):
    if right_justified:
        pat = r"([ ]*[^ ]*)"
    else:
        pat = r"([^ ]*[ ]*)"
    u = reduce(lambda a, b: a + [a[-1:][0] + b],
               [len(e) for e in re.split(pat, template) if e != ""],
               [0])
    return [(u[e], u[e + 1]) for e in range(len(u) - 1)]


def get_userid_from_s_dn(dn):
    l = [e for e in dn.split(',') if e.startswith("CN=")]
    if len(l) != 1:
        return None
    cn = l[0][3:]
    if x509_usermap is None:
        return cn
    return x509_usermap.get(cn)


x509_usermap = None


def load_x509_usermap(path):
    try:
        with open(path, "r") as f:
            r = [(e[0].strip(), e[1].strip())
                    for e in [e.split('\t') for e in f.readlines()] ]
            set_x509_usermap(dict(r))
    except Exception as e:
        pass


def set_x509_usermap(d):
    global x509_usermap
    x509_usermap = d


class MachineStatus(BaseModel):
    system_status: str


def parseToMachineStatus(e):
    fields = ["system_status"]
    l = e.split()
    if len(l) != len(fields):
        return None
    return MachineStatus(**dict(zip(fields, l)))


class SubmitJobRequest(BaseModel):
    jobfile: str = None
    qopt: str = None


class Command(BaseModel):
    command: str


def normalize_time(a):
    m = re.search(r"([0-9][0-9]*):([0-9][0-9]*):([0-9][0-9]*)", a)
    if m is not None:
        hour = int(m.group(1))
        min = int(m.group(2))
        sec = int(m.group(3))
        return (f"{hour:04d}:{min:02d}:{sec:02d}")
    m = re.search(r"([0-9][0-9]*):([0-9][0-9]*)", a)
    if m is not None:
        hour = 0
        min = int(m.group(1))
        sec = int(m.group(2))
        return f"{hour:04d}:{min:02d}:{sec:02d}"
    return a


def normalize_date(a):
    m = re.search(r"([0-9][0-9]*)/([0-9][0-9]*) ([0-9][0-9]*):([0-9][0-9]*):([0-9][0-9]*)", a)
    if m is not None:
        l = time.localtime()
        mon = int(m.group(1))
        mday = int(m.group(2))
        hour = int(m.group(3))
        min = int(m.group(4))
        sec = int(m.group(5))
        t = (l.tm_year, mon, mday, hour, min, sec, 0, 0, 0)
        return time.strftime("%Y-%m-%dT%H:%M:%S", t)
    m = re.search(r"([0-9][0-9]*)/([0-9][0-9]*) ([0-9][0-9]*):([0-9][0-9]*)", a)
    if m is not None:
        l = time.localtime()
        mon = int(m.group(1))
        mday = int(m.group(2))
        hour = int(m.group(3))
        min = int(m.group(4))
        t = (l.tm_year, mon, mday, hour, min, 0, 0, 0, 0)
        return time.strftime("%Y-%m-%dT%H:%M:%S", t)
    try:
        m = time.strptime(a, "%Y-%m-%dT%H:%M:%S")
        if m is not None:
            return time.strftime("%Y-%m-%dT%H:%M:%S", m)
    except:
        pass
    try:
        m = time.strptime(a, "%a %b %d %H:%M:%S %Y")
        if m is not None:
            return time.strftime("%Y-%m-%dT%H:%M:%S", m)
    except:
        pass
    return a


def realpath(path):
    return os.path.join(".", path)
