# Steps to generate a static HTML file from openapi.json

This is the procedure for CentOS Linux release 7.9.2009.

## Preparations in advance
### Install YARN
```bash
$ curl -L -O https://rpm.nodesource.com/pub/el/NODESOURCE-GPG-SIGNING-KEY-EL
$ sudo mv -i NODESOURCE-GPG-SIGNING-KEY-EL /etc/pki/rpm-gpg/
$ sudo rpm --import /etc/pki/rpm-gpg/NODESOURCE-GPG-SIGNING-KEY-EL
$ rpm -qai gpg-pubkey* | less

$ curl -fsSL https://rpm.nodesource.com/setup_current.x | sudo bash -

$ curl -sL https://dl.yarnpkg.com/rpm/yarn.repo | sudo tee /etc/yum.repos.d/yarn.repo
$ sudo yum install yarn
```

### Install ReDoc
```bash
$ mkdir static
$ cd static

$ yarn add redoc
$ yarn add redoc-cli
$ yarn list redoc redoc-cli
```

## Convert
### Download openapi.json file from REST API SERVER
```bash
$ curl -L -O http://localhost:8000/openapi.json
```

### (OPTIONAL) Launch a local server and check via HTTP
```bash
$ npx redoc-cli serve openapi.json --watch

  See http://localhost:8080/ in your web browser.
  Press CTRL + c to stop.
```

### Convert to static HTML file
```bash
$ npx redoc-cli bundle openapi.json -o hpc-rest-api.html
```

