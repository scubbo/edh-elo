#!/usr/bin/env bash

# Idempotent
source .venv/bin/activate
uvicorn app:app --reload
