#!/usr/bin/env bash
gunicorn -b 0.0.0.0:8000 -w 1 app:app -k gevent \
    --error-logfile ./logs/gunicorn/app/app.log \
    --log-file ./logs/gunicorn/app/app.log \
    --access-logfile ./logs/gunicorn/access/access.log \
    --log-level=warning \
    --enable-stdio-inheritance