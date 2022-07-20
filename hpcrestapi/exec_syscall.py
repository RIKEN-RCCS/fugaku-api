import datetime
import json
import array
import os
import socket
import stat
import subprocess
import sys

"""
open
   success always
            exit code 0


listdir
   success: write directory listing in json  to stdout
            exit code 0
   fail:    write Exception.args in json to stderr
            exit code 1


chmod
   success: no output
            exit code 0
   fail:    write Exception.args in json to stderr
            exit code 1


mkdir
   success: no output
            exit code 0
   fail:    write Exception.args in json to stderr
            exit code 1


system_status
   success: print system status
            exit code 0
   never fail


submit
   success: exit code 0
   fail:    exit code 1
   stdout, stderr == remain


shell
   success: shell
            shell stdout is redicred to stdout
            shell stderr is recirected to stderr
            exit code  ==  inner shell's exit code

   fail:    write Exception.args in json to stderr
            exit code 1


unknown command (first argument)
   always fail
            output none
            exit code  126


too few arguments
    always fail
            no output
            exit code  1


extra arguments (not checked)
    does not affect command behaviour

"""


def main():
    args = sys.argv[1:]

    try:
        os.chdir(os.path.expanduser("~"))
        if args[0] == "open":
            call_open(args[1], int(args[2]), int(args[3]))
        elif args[0] == "listdir":
            call_listdir(args[1])
        elif args[0] == "chmod":
            call_chmod(args[1], args[2])
        elif args[0] == "mkdir":
            call_mkdir(args[1], args[2])
        elif args[0] == "system_status":
            call_system_status()
        elif args[0] == "submit":
            call_submit(args[1], args[2])
        elif args[0] == "shell":
            shell_exec()
        else:
            sys.exit(126)
    except Exception as e:
        sys.stderr.write(f"{json.dumps(e.args)}")
        sys.exit(1)
    sys.exit(0)


def call_open(path, flags, mode):
    sock = socket.socket(fileno=1)
    try:
        d = os.open(path, flags, mode=mode)
        cmsg_level = socket.SOL_SOCKET
        cmsg_type = socket.SCM_RIGHTS
        cmsg_data = array.array("i", [d])
        ancdata = (cmsg_level, cmsg_type, cmsg_data)
        retcode = array.array("i", [0])
        sock.sendmsg([retcode], [ancdata])
    except Exception as e:
        errno, _ = e.args
        retcode = array.array("i", [errno])
        sock.sendmsg([retcode], [])
        # always success


def call_listdir(path):
    r = os.listdir(path=path)
    print(f"{json.dumps([se(path, ent) for ent in r])}")


def se(path, ent):
    try:
        r = os.stat(os.path.join(path, ent))
    except OSError:
        return ino(ent, 0, 0)
    return ino(ent, r.st_mode, int(r.st_mtime))


def ino(ent, mode, mtime):
    return {"path": ent,
            "st_mode": stat.filemode(mode),
            "st_mtime": mystrftime(int(mtime))}


def mystrftime(s):
    return datetime.datetime.fromtimestamp(s).strftime("%Y-%m-%dT%H:%M:%S")


def call_chmod(path, mode):
    os.chmod(path, int(mode, 8))


def call_mkdir(path, mode):
    os.mkdir(path, mode=int(mode, 8))


def call_system_status():
    print("OK", end="")


def call_submit(sub_command, script):
    cmd = [sub_command, script]
    proc = subprocess.Popen(cmd, stdin=None)
    proc.communicate()
    sys.exit(proc.returncode)


def shell_exec():
    cmd = sys.stdin.read()
    proc = subprocess.Popen(cmd, shell=True, stdin=None)
    proc.communicate()
    sys.exit(proc.returncode)


if __name__ == "__main__":
    main()
