#!/bin/sh

ssh-keygen -b 4096 -t rsa -C "github-website-update@intranet.nipe-systems.de" -N "" -f github-website-update
mv github-website-update{,.key}
git clone https://github.com/carlos-jenkins/python-github-webhooks.git
docker build -t github-website-update .
