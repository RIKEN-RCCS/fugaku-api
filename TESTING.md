# HPC REST API Testing

HPC REST API comes with a unittest.
To run unittest, install pytest and run pytest.

Each test except for test_common.py checks API's response against a 
given http request.

Following are the tests to be run by pytest:

    api/tests/common.py
    api/tests/hpc_system/test_hpc_system_groups.py
    api/tests/hpc_system/test_hpc_system_users.py
    api/tests/hpc_system/test_hpc_system_admin.py
    api/tests/hpc_system/test_hpc_system_status.py
    api/tests/file/test_file_list.py
    api/tests/file/test_file_download.py
    api/tests/file/test_file_upload.py
    api/tests/file/test_file_mkdir.py
    api/tests/file/test_file_chmod.py
    api/tests/jobs/test_job_list.py
    api/tests/jobs/test_job_detail.py
    api/tests/jobs/test_job_submit.py
    api/tests/jobs/test_job_delete.py
    api/tests/user_command/test_user_command.py


Following test checks get_authorized_user functionality.

    api/tests/test_common.py

--EOF
