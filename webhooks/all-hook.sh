#!/bin/sh

ssh -o UserKnownHostsFile=/app/known_hosts -i github-website-update.key root@nipe-systems.de 'cd /root/nipe-systems.de && git pull && /root/nipe-systems.de/deploy.sh /srv/http'
