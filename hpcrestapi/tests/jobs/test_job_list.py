from hpcrestapi.tests.common import common_test
from hpcrestapi.tests.common import jwttoken
from hpcrestapi.main import app
from fastapi.testclient import TestClient
import os

client = TestClient(app)


##### FUGAKU JOBS/LIST #########################################################
def test_job_detail_fugaku():
    spec = {
        "system_type": "fugaku",

        "method": "get",
        "uri": "/jobs/",
        "expected_status_code": 200,
        "expected_response_json":

[{'job_id': '6291500', 'job_name': 'job1.sh', 'status': 'RNA', 'user': 'a03010', 'group': 'rccs-aot', 'start_date': '2021-04-12T11:25:00', 'elapse_time': '0000:00:00', 'node_require': '12', 'priority': '127', 'accept': '2021-04-12T11:25:50', 'queue': 'small', 'Fugaku:elapse_limit': '0000:01:00', 'Fugaku:md': 'NM', 'Fugaku:vnode': '-', 'Fugaku:core': '-', 'Fugaku:v_mem': '-', 'Fugaku:v_pol': '-', 'Fugaku:e_pol': '-', 'Fugaku:rank': 'bychip', 'Fugaku:lst': 'QUE', 'Fugaku:ec': '0', 'Fugaku:pc': '0', 'Fugaku:sn': '0', 'Fugaku:reason': '-'}, {'job_id': '6291501', 'job_name': 'job1.sh', 'status': 'RNA', 'user': 'a03010', 'group': 'rccs-aot', 'start_date': '2021-04-12T11:25:00', 'elapse_time': '0000:00:00', 'node_require': '12', 'priority': '127', 'accept': '2021-04-12T11:25:51', 'queue': 'small', 'Fugaku:elapse_limit': '0000:01:00', 'Fugaku:md': 'NM', 'Fugaku:vnode': '-', 'Fugaku:core': '-', 'Fugaku:v_mem': '-', 'Fugaku:v_pol': '-', 'Fugaku:e_pol': '-', 'Fugaku:rank': 'bychip', 'Fugaku:lst': 'QUE', 'Fugaku:ec': '0', 'Fugaku:pc': '0', 'Fugaku:sn': '0', 'Fugaku:reason': '-'}],

        "authorization": jwttoken(),

        "expected_popen_args": ["*/timeout", "250",
                       "*/sudo", "-u", "nobody",
                       "pjstat", "-v"],
        "communicate_return_value": (
b"""JOB_ID     JOB_NAME   MD ST  USER     GROUP    START_DATE      ELAPSE_TIM ELAPSE_LIM            NODE_REQUIRE    VNODE  CORE V_MEM        V_POL E_POL RANK      LST EC  PC  SN PRI ACCEPT         RSC_GRP  REASON          
6291500    job1.sh    NM RNA a03010   rccs-aot (04/12 11:25)   0000:00:00 0000:01:00            12              -      -    -            -     -     bychip    QUE 0   0   0  127 04/12 11:25:50 small    -               
6291501    job1.sh    NM RNA a03010   rccs-aot (04/12 11:25)   0000:00:00 0000:01:00            12              -      -    -            -     -     bychip    QUE 0   0   0  127 04/12 11:25:51 small    -               
""",
                b""),
        "returncode": 0,
    }
    common_test(client, spec)


##### SLURM JOBS/LIST ##########################################################
def test_job_detail_slurm():
    spec = {
        "system_type": "slurm",

        "method": "get",
        "uri": "/jobs/",
        "expected_status_code": 200,
        "expected_response_json":
[{'job_id': '92', 'job_name': 'job1.sh', 'status': 'PD', 'user': '1321', 'group': '200', 'elapse_time': '0000:00:00', 'node_require': '1', 'priority': '4294901669', 'accept': '2021-04-12T11:29:26', 'queue': 'dvl', 'Slurm:ACCOUNT': '(null)', 'Slurm:GRES': '(null)', 'Slurm:MIN_CPUS': '1', 'Slurm:MIN_TMP_DISK': '0', 'Slurm:END_TIME': 'N/A', 'Slurm:FEATURES': '(null)', 'Slurm:OVER_SUBSCRIBE': 'OK', 'Slurm:COMMENT': '(null)', 'Slurm:TIME_LIMIT': 'UNLIMITED', 'Slurm:MIN_MEMORY': '0', 'Slurm:REQ_NODES': '', 'Slurm:COMMAND': '/home/nis/ubi/job1.sh', 'Slurm:QOS': '(null)', 'Slurm:REASON': 'Resources', 'Slurm:RESERVATION': '(null)', 'Slurm:WCKEY': '(null)', 'Slurm:EXC_NODES': '', 'Slurm:NICE': '0', 'Slurm:S:C:T': '*:*:*', 'Slurm:EXEC_HOST': 'n/a', 'Slurm:CPUS': '1', 'Slurm:DEPENDENCY': '', 'Slurm:ARRAY_JOB_ID': '92', 'Slurm:SOCKETS_PER_NODE': '*', 'Slurm:CORES_PER_SOCKET': '*', 'Slurm:THREADS_PER_CORE': '*', 'Slurm:ARRAY_TASK_ID': 'N/A', 'Slurm:TIME_LEFT': 'UNLIMITED', 'Slurm:NODELIST': '', 'Slurm:CONTIGUOUS': '0', 'Slurm:NODELIST(REASON)': '(Resources)', 'Slurm:START_TIME': 'N/A', 'Slurm:STATE': 'PENDING', 'Slurm:LICENSES': '(null)', 'Slurm:CORE_SPEC': 'N/A', 'Slurm:SCHEDNODES': '(null)', 'Slurm:WORK_DIR': '/home/nis/ubi'}, {'job_id': '93', 'job_name': 'job1.sh', 'status': 'PD', 'user': '1321', 'group': '200', 'elapse_time': '0000:00:00', 'node_require': '1', 'priority': '4294901668', 'accept': '2021-04-12T11:29:27', 'queue': 'dvl', 'Slurm:ACCOUNT': '(null)', 'Slurm:GRES': '(null)', 'Slurm:MIN_CPUS': '1', 'Slurm:MIN_TMP_DISK': '0', 'Slurm:END_TIME': 'N/A', 'Slurm:FEATURES': '(null)', 'Slurm:OVER_SUBSCRIBE': 'OK', 'Slurm:COMMENT': '(null)', 'Slurm:TIME_LIMIT': 'UNLIMITED', 'Slurm:MIN_MEMORY': '0', 'Slurm:REQ_NODES': '', 'Slurm:COMMAND': '/home/nis/ubi/job1.sh', 'Slurm:QOS': '(null)', 'Slurm:REASON': 'Resources', 'Slurm:RESERVATION': '(null)', 'Slurm:WCKEY': '(null)', 'Slurm:EXC_NODES': '', 'Slurm:NICE': '0', 'Slurm:S:C:T': '*:*:*', 'Slurm:EXEC_HOST': 'n/a', 'Slurm:CPUS': '1', 'Slurm:DEPENDENCY': '', 'Slurm:ARRAY_JOB_ID': '93', 'Slurm:SOCKETS_PER_NODE': '*', 'Slurm:CORES_PER_SOCKET': '*', 'Slurm:THREADS_PER_CORE': '*', 'Slurm:ARRAY_TASK_ID': 'N/A', 'Slurm:TIME_LEFT': 'UNLIMITED', 'Slurm:NODELIST': '', 'Slurm:CONTIGUOUS': '0', 'Slurm:NODELIST(REASON)': '(Resources)', 'Slurm:START_TIME': 'N/A', 'Slurm:STATE': 'PENDING', 'Slurm:LICENSES': '(null)', 'Slurm:CORE_SPEC': 'N/A', 'Slurm:SCHEDNODES': '(null)', 'Slurm:WORK_DIR': '/home/nis/ubi'}]
,

        "authorization": jwttoken(),

        "expected_popen_args": ["*/timeout", "250",
                       "*/sudo", "-u", "nobody",
                       "squeue", "--format=%all", "-u", "nobody"],
        "communicate_return_value": (
b"""ACCOUNT|GRES|MIN_CPUS|MIN_TMP_DISK|END_TIME|FEATURES|GROUP|OVER_SUBSCRIBE|JOBID|NAME|COMMENT|TIME_LIMIT|MIN_MEMORY|REQ_NODES|COMMAND|PRIORITY|QOS|REASON||ST|USER|RESERVATION|WCKEY|EXC_NODES|NICE|S:C:T|JOBID|EXEC_HOST|CPUS|NODES|DEPENDENCY|ARRAY_JOB_ID|GROUP|SOCKETS_PER_NODE|CORES_PER_SOCKET|THREADS_PER_CORE|ARRAY_TASK_ID|TIME_LEFT|TIME|NODELIST|CONTIGUOUS|PARTITION|PRIORITY|NODELIST(REASON)|START_TIME|STATE|USER|SUBMIT_TIME|LICENSES|CORE_SPEC|SCHEDNODES|WORK_DIR
(null)|(null)|1|0|N/A|(null)|member|OK|92|job1.sh|(null)|UNLIMITED|0||/home/nis/ubi/job1.sh|0.99998472025618|(null)|Resources||PD|nis|(null)|(null)||0|*:*:*|92|n/a|1|1||92|200|*|*|*|N/A|UNLIMITED|0:00||0|dvl|4294901669|(Resources)|N/A|PENDING|1321|2021-04-12T11:29:26|(null)|N/A|(null)|/home/nis/ubi
(null)|(null)|1|0|N/A|(null)|member|OK|93|job1.sh|(null)|UNLIMITED|0||/home/nis/ubi/job1.sh|0.99998472002335|(null)|Resources||PD|nis|(null)|(null)||0|*:*:*|93|n/a|1|1||93|200|*|*|*|N/A|UNLIMITED|0:00||0|dvl|4294901668|(Resources)|N/A|PENDING|1321|2021-04-12T11:29:27|(null)|N/A|(null)|/home/nis/ubi
""",
                b""),
        "returncode": 0,
    }
    common_test(client, spec)


##### TORQUE JOBS/LIST #########################################################
def test_job_detail_torque():
    spec = {
        "system_type": "torque",

        "method": "get",
        "uri": "/jobs/",
        "expected_status_code": 200,
        "expected_response_json":
[{'job_id': '94', 'job_name': 'job1.sh', 'status': 'Q', 'user': 'nis(1321)', 'group': 'member(200)', 'start_date': '2021-04-12T11:31:53', 'priority': '4294901667', 'queue': 'dvl', 'Torque:JobOwner': 'nis@dvl3-01', 'Torque:Resource_List.walltime': '71582788:15:00', 'Torque:Resource_List.nodect': '1', 'Torque:Resource_List.ncpus': '1'}, {'job_id': '95', 'job_name': 'job1.sh', 'status': 'Q', 'user': 'nis(1321)', 'group': 'member(200)', 'start_date': '2021-04-12T11:31:53', 'priority': '4294901666', 'queue': 'dvl', 'Torque:JobOwner': 'nis@dvl3-01', 'Torque:Resource_List.walltime': '71582788:15:00', 'Torque:Resource_List.nodect': '1', 'Torque:Resource_List.ncpus': '1'}]
,

        "authorization": jwttoken(),

        "expected_popen_args": ["*/timeout", "250",
            "*/sudo", "-u", "nobody",
            "qstat", "-f"],
        "communicate_return_value": (
b"""Job Id:	94
	Job_Name = job1.sh
	Job_Owner = nis@dvl3-01
	job_state = Q
	queue = dvl
	qtime = Mon Apr 12 11:31:53 2021
	Priority = 4294901667
	euser = nis(1321)
	egroup = member(200)
	Resource_List.walltime = 71582788:15:00
	Resource_List.nodect = 1
	Resource_List.ncpus = 1

Job Id:	95
	Job_Name = job1.sh
	Job_Owner = nis@dvl3-01
	job_state = Q
	queue = dvl
	qtime = Mon Apr 12 11:31:53 2021
	Priority = 4294901666
	euser = nis(1321)
	egroup = member(200)
	Resource_List.walltime = 71582788:15:00
	Resource_List.nodect = 1
	Resource_List.ncpus = 1

""",
                b""),
        "returncode": 0,
    }
    common_test(client, spec)
