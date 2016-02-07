#!/usr/bin/env bash
gunicorn -b 0.0.0.0:8000 -w 1 app:app -k gevent \
    --log-file ./gunicorn-logs/app/app.log \
    --access-logfile ./gunicorn-logs/access/access.log \
    --log-level=debug \
    --enable-stdio-inheritance