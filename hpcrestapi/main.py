'''
'''
from fastapi import FastAPI

import os
import sys
import yaml
import logging
import logging.config
from pathlib import Path
from hpcrestapi import config

from hpcrestapi import common
from hpcrestapi.system.sys_config import load_system_function

config_file: str = None
config_all = None
config_hpc_rest_api = None
config_hpc_rest_api_server = None


# read configuration file
config_file = common.complete_path("config/config.yaml")
try:
    with open(config_file) as file:
        config_all = yaml.safe_load(file)
except yaml.YAMLError as err:
    if hasattr(err, 'problem_mark'):
        mark = err.problem_mark
        print(f"Error in {config_file} at line {mark.line+1}, column {mark.column+1}")
    (_, _, message, _) = err.args
    print(f"ERROR: {message}")
    sys.exit(1)
except Exception as err:
    print('Exception occured loading configuration file', file=sys.stderr)
    sys.exit(1)

config.settings.conf = config_all
system_type = config_all["HPC_REST_API_SERVER"]["system_type"]
load_system_function(system_type)

config.settings.conf = config_all
x509_usermap_path = config_all["HPC_REST_API_SERVER"]["x509_usermap"]
common.load_x509_usermap(common.complete_path(x509_usermap_path))

# logging conf
logging.config.dictConfig(config_all['LOGGING'])
logger = logging.getLogger('hpcrestapi')
#print('# logging: ', config_all['LOGGING'])

# hpc rest api server conf
config_hpc_rest_api_server = config_all['HPC_REST_API_SERVER']
#print('# config_hpc_rest_api_server: ', config_hpc_rest_api)

# hpc rest api conf
config_hpc_rest_api = config_all['HPC_REST_API']
#print('# config_hpc_rest_api: ', config_hpc_rest_api)


#default_response_class = ORJSONResponse デフォルトの応答クラスを指定
app = FastAPI(
    debug=True,
    title='HPC REST API',
    version='1.0.0'
)
origins = [
    'https://www.fugaku.r-ccs.riken.jp',
]


#
# add routers
#


# ジョブ操作
from hpcrestapi.jobs import job_submit
from hpcrestapi.jobs import job_cancel
from hpcrestapi.jobs import job_list
from hpcrestapi.jobs import job_detail
app.include_router(job_submit.router)
app.include_router(job_cancel.router)
app.include_router(job_list.router)
app.include_router(job_detail.router)
# ファイル操作
from hpcrestapi.file import file_upload
from hpcrestapi.file import file_download
from hpcrestapi.file import file_list
from hpcrestapi.file import file_chmod
from hpcrestapi.file import file_mkdir
app.include_router(file_upload.router)
app.include_router(file_download.router)
app.include_router(file_list.router)
app.include_router(file_chmod.router)
app.include_router(file_mkdir.router)
# コマンド操作
from hpcrestapi.user_command import user_command
app.include_router(user_command.router)
# HPC システム操作
from hpcrestapi.hpc_system import hpc_system_status
from hpcrestapi.hpc_system import hpc_system_users
from hpcrestapi.hpc_system import hpc_system_groups
from hpcrestapi.hpc_system import hpc_system_admin
app.include_router(hpc_system_status.router)
app.include_router(hpc_system_users.router)
app.include_router(hpc_system_groups.router)
app.include_router(hpc_system_admin.router)


#
# setting event
#
@app.on_event('startup')
async def startup_event():
    logger = logging.getLogger('hpcrestapi')
    logger.info('Ready')


@app.on_event('shutdown')
def shutdown_event():
    #logger = logging.getLogger('hpcrestapi')
    logger.info('Shutdown')


if __name__ == '__main__':
    #logger = logging.getLogger('hpcrestapi')
    config_all = None
    config_hpc_rest_api_server = config_all['HPC_REST_API_SERVER']
    config_hpc_rest_api = config_all['HPC_REST_API']

    logger.info('Start')
    uvicorn.run('app:main',
                 host=config_hpc_rest_api_server['hostname'],
                 port=config_hpc_rest_api_server['port'],
                 log_level='info')
    logger.info('Finished')
