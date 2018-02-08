#!/bin/sh

cd webhook-server
source venv/bin/activate
python webhooks.py
deactivate
