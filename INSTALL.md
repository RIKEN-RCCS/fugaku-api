# HPC REST API Installation


*Requirements*: FastAPI requires Python 3.6+, so please prepare an environment of Python 3.6 or higher.


## 1. Download HPC REST API
```bash
cd $HOME/work
git clone git@gitlab.ops.r-ccs.riken.jp:soum/hpc-rest-api.git
```


## 2. Install Prerequisites
```bash
pip3 install -r hpc-rest-api/requirements.txt
```


## 3. HTTP Server

### 3.1. NginX

#### 3.1.1. install NginX
```bash
sudo apt install -y nginx
```

#### 3.1.2. NginX configuration example

**NginX Setting Example**:
```bash
--- /etc/nginx/sites-available/default	2018-04-06 14:31:11.000000000 +0900
+++ default	2021-04-21 10:54:40.415369396 +0900
@@ -89,3 +89,30 @@
 #		try_files $uri $uri/ =404;
 #	}
 #}
+
+server {
+	listen 443 ssl;
+	server_name fastapitest;
+
+	proxy_set_header Host $host;
+	proxy_set_header X-Forwarded-Host $host;
+	proxy_set_header X-Forwarded-Proto $scheme;
+	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
+	proxy_set_header X-Real-IP $remote_addr;
+
+	proxy_set_header X-SSL-Client-S-Dn $ssl_client_s_dn;
+	proxy_set_header X-SSL-Client-Verify $ssl_client_verify;
+
+	ssl_certificate_key "/etc/nginx/server_certificates/server.key";
+	ssl_certificate "/etc/nginx/server_certificates/server.crt";
+
+	ssl_client_certificate "/etc/nginx/client_certificates/ca.crt";
+	ssl_verify_client on;
+
+	location / {
+		proxy_pass http://127.0.0.1:8000/;
+	}
+}
```

#### 3.1.3. restart NginX
```bash
sudo service nginx restart
```

### 3.2. Apache2

#### 3.2.1. install Apache2
```bash
sudo apt install -y apache2
sudo a2enmod ssl
sudo a2enmod rewrite
sudo a2enmod proxy_http
sudo a2enmod headers
```

#### 3.2.2. Apache2 configuration example
**Apache2 Setting Example**:
```bash
cat <<EOF > /etc/apache2/sites-enabled/mysite.conf
ServerName 127.0.0.1
<VirtualHost *:443>
	SSLEngine on
	SSLCertificateFile /etc/apache2/server_certificates/server.crt
	SSLCertificateKeyFile /etc/apache2/server_certificates/server.key
	SSLCACertificateFile /etc/apache2/client_certificates/ca.crt
	SSLVerifyClient require
	DocumentRoot /var/www/html
	ServerAdmin root@localhost

	<Directory "/var/www/html">
		AllowOverride FileInfo AuthConfig Limit Indexes
		Options MultiViews Indexes SymLinksIfOwnerMatch Includes
		AllowOverride All
		Require all granted
	</Directory>

	RequestHeader set X-SSL-CLIENT-S-Dn "%{SSL_CLIENT_S_DN}s"
	RequestHeader set X-SSL-Client-Verify "%{SSL_CLIENT_VERIFY}s"

	RewriteEngine on
	ProxyPass / http://127.0.0.1:8000/
	ProxyPreserveHost on

</VirtualHost>
EOF
```

#### 3.2.3. restart Apache2
```bash
sudo service apache2 restart
```


## 4. Install package and Create configuration file
```bash
pip install -e .

cp $HOME/work/hpc-rest-api/config/config-sample.yaml \
   $HOME/work/hpc-rest-api/config/config.yaml

vi $HOME/work/hpc-rest-api/config/config.yaml

    hostname: 0.0.0.0
    port: 8000
    LOGGING.handers.file.filename: /var/log/rest_api_server.log # log file path
```

## 5 Create x509_usermap

`config/x509_usermap` maps ssl user to unix username.  If ssl username and unix username are identical always, `x509_usermap`
may be absent.

`x509_usermap` consists of a tab separated ssl username and unix username, one per user.  All users must be listed in this file, as missing user is treated unauthorized.

NOTE: `x509_usermap` is read once when the system starts running.

```
cat <<EOF ssl_user	system_user' > $HOME/work/hpc-rest-api/config/x509_usermap
alice	a271828
bob	a314159
EOF
```

## 6. Configure hpc_system/status

The hpc_system/status API is expected to return current system status to client.  Hpc_system/status acquires system status value by executing following command:

```bash
"command/exec_syscall system_status"
```

The command "command/exec_syscall system_status" is shipped with a sample function that responds "OK" always.  To customize "command/exec_syscall system_status", modify function "call_system_status" in hpcrestapi/exec_syscall.py.



## 7. Run gunicorn (NginX, Apache2)

```bash
gunicorn -D \
    -w 4 \
    -k uvicorn.workers.UvicornWorker \
    hpcrestapi.main:app \
    --bind localhost:8000
```



## API documentation in the following location:

 - SWAGGER UI:
    http://127.0.0.1:8000/docs

 - ReDoc:
    http://127.0.0.1:8000/redoc


## Reference
- FastAPI installation https://fastapi.tiangolo.com/#installation

