FROM python:3

WORKDIR /app

COPY python-github-webhooks/requirements.txt /app
COPY config.json /app
COPY python-github-webhooks/webhooks.py /app
COPY all-hook.sh /app/hooks/all
COPY github-website-update.key /app
COPY known_hosts /app

RUN pip install -r requirements.txt

EXPOSE 5000
CMD [ "python", "webhooks.py" ]
