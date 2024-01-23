#!/usr/bin/env bash

# Idempotent
source .venv/bin/activate
FLASK_APP=app SECRET_KEY=super-secret flask run
