#!/bin/sh

cd webhook-server
git init
git remote add origin https://github.com/carlos-jenkins/python-github-webhooks.git
git fetch origin
git checkout -b master --track origin/master
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
