# Setting Example - config.yaml

```
#
# HPC REST API Server configuration
#
HPC_REST_API_SERVER:
  hostname: 0.0.0.0                                # REST API server IP address
  port: 8000                                       # REST API server TCP port number
  sudo:
    exec_syscall_path: 'command/exec_syscall'      # Set exec_syscall path (relative to package's parent dir)
    exec_cmd_timeout: 250                          # Set command timeout (sec)
    sudo_path: '/usr/bin/sudo'                     # Set sudo command full path
    timeout_path: '/usr/bin/timeout'               # Set timeout command full path
  x509_usermap: 'config/x509_usermap'              # Set user mapping path (relative to package's parent dir)
  system_type: "slurm"                             # Select the workload manager type from fugaku, slurm and torque
  ssl_client_s_dn: "x-ssl-client-s-dn"             # Set the HTTP HEADER name where the user name authenticated by client authentication is saved
  ssl_client_verify: "x-ssl-client-verify"         # Set the HTTP HEADER name to save the result of client authentication
  version: '0.1.0'                                 # REST API version


#
# Logging configuration
#    See also https://docs.python.org/3.9/library/logging
#
LOGGING:
  version: 1
  formatters:                                      # Formatters specify the layout of log records in the final output
    simple:
      format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
      datefmt: '%Y/%m/%d %H:%M:%S'
  handlers:                                        # Handlers send the log records (created by loggers) to the appropriate destination
    console:
      class: logging.StreamHandler
      formatter: simple
      level: DEBUG
      stream: ext://sys.stdout
    file:
      class: logging.FileHandler
      formatter: simple
      filename: /var/log/rest_api_server.log       # Specifies that a FileHandler be created, using the specified filename, rather than a StreamHandler
      mode: a                                      # If filename is specified, open the file in this mode. Defaults to 'a'
  loggers:                                         # Loggers expose the interface that application code directly uses
    root:
      level: DEBUG
      handlers: [console]
      propagate: no
    api:
      level: INFO
      handlers: [console, file]
      propagate: 0
      qualname: api
  root:
    level: DEBUG
    handlers: []
```
