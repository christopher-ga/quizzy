#!/bin/bash

# Generate random secret key
echo SECRET_KEY=$(echo $RANDOM | sha256sum |head -c 64) > .env

# Run the quiz app
gunicorn -k eventlet -b 0.0.0.0:8000 wsgi:app
