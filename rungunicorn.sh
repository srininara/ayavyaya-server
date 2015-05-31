#!/usr/bin/env bash
gunicorn -w 1 app:app -k gevent \
    --log-file ./gunicorn-logs/app/app.log \
    --access-logfile ./gunicorn-logs/access/access.log \
    --log-level=debug \
    --enable-stdio-inheritance