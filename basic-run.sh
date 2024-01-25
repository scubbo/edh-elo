#!/usr/bin/env bash

# Idempotent
source .venv/bin/activate
# `--debug` enables live-refresh
FLASK_APP=app SECRET_KEY=super-secret flask --debug run
