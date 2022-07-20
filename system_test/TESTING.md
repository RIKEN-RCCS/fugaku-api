# System Testing

## Overview

System testing includes running hpc-rest-api server and hpccli to confirm
everything go well in situ.  The procedure is as following:
(1) Setup hpc-rest-api
(2) Run hpccli by script and check output.

## 1. Install hpc-rest-api

Refer hpc-rest-api/INSTALL.md and install hpc-rest-api.
For http server, choose Apache2 or/and NginX that matches to your needs.
Make sure your http server is awaiting at "https://127.0.0.1".

## 2. Configure test script

Configure 'cnf' to match your environment.

USER=         ... real user for testing
PASS=secret   ... this test does not use password. do not change.
ENDPOINT=     ... the location where your http server is awaiting at.
CERTIFICATE=  ... your certificate, that is accepted by your http server.
PRIVATEKEY=   ... your private key for the certificate.
HPCCLI=       ... "hpccli" or "/path/to/hpccli" (absolute path may be better)

Review 'tst' trough. 

The script consists four pars: (1) preamble which setups
environment variables, (2) testing with client certificate authentication,
(3) testing with jwtToken authentication, (4) testing with basic authentication.

The script will pause between part (1) and (2). You must start http server
with SSLVerifyClient enabled at this point.

The script will pause again between part (2) and (3). You must (re)start http 
server with SSLVerifyClient disabled.


## 3. Run test script

Following test will be run in order at part (2). 
Check each test output correctness.

hpccli system status
	will print {"message": "OK"}

hpccli file list
	will list your $HOME

hpccli command
	will print {"retcode":0,"stdout":"[$HOSTNAME $HOME $DATE]\n","stderr":""}

hpccli system admin
	ditto.

hpccli system get group
	will print groups that you are belongs to.

hpccli system get user
	will print your pwent info.

hpccli job list
	will print empty list (or if you have running jobs, job list)


Following three tests will be run in order at part (3) and part (4)
Check each test output correctness, following above description.

hpccli system status
hpccli system get group
hpccli system admin

Fin.
