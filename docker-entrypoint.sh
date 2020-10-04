#!/bin/sh
set -e
gunicorn -c gunicorn.config.py wsgi:app
