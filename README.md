# nipe-systems.de website continuous deployment

This repository includes all files that are needed for the continuous deployment of the NIPE-SYSTEMS website. A author may push a new version of parts of the website to this repository. This triggers a completely autonomous deployment to the web server. This architecture automates the following steps:

1. User modifies files
2. User commits and pushes files to remote repository
3. **GitHub triggers architecture via webhook**
4. **Webhook server triggers webserver update**
5. **Webserver pulls files and generates current version of the website**

## Website deployment

When new files are pushed to this repository trigger `git pull` and then execute:

```bash
./deploy.sh /srv/http
```

where `/srv/http` is the deploy folder where the www-root is located. The deploy script does the following steps:

1. Copy files to webserver directory
2. Generate index file

More to be added in the future.

## Webhooks server

The webhooks server requires [Docker](https://docker.com) to be installed. The server runs an unsecure HTTP and is configured to not check GitHub-IPs. It is designed to run behind a reverse proxy which handles TLS and access limitations.

```bash
cd webhooks
# create file `known_hosts` with the SSH fingerprint
./init.sh
```

The container can be started e.g.:

```bash
docker run -it -d --restart always --name github-website-update -p 5000:5000 github-website-update
```

A reverse proxy may be configured with:

```nginx
location / {
	proxy_set_header Host $host:$server_port;
	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	proxy_pass http://1.2.3.4:5000/;
	proxy_redirect off;
	proxy_http_version 1.1;
	proxy_request_buffering off;
	
	# IPs from https://api.github.com/meta
	allow 192.30.252.0/22;
	allow 185.199.108.0/22;
	deny all;
	
	# only allow POST
	limit_except POST {
		deny all;
	}
}
```
