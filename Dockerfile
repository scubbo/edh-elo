# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.9.6
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Create writeable directory for database
USER root
RUN mkdir database
RUN chmod 755 database
RUN chown appuser:appuser database
USER appuser

EXPOSE 8000


########
# Targets diverge from here
########

FROM base as prod

COPY . .
CMD uvicorn app:app --host 0.0.0.0

###

FROM base as dev
# You probably want sqlite3 to poke around with the database anyway
USER root
RUN apt update
RUN apt install sqlite3
USER appuser
# Expects that the source code will be mounted into the container
CMD uvicorn app:app --reload --host 0.0.0.0
