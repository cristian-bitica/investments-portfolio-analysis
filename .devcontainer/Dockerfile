
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Install additional packages
RUN apt update && export DEBIAN_FRONTEND=noninteractive \
    && apt -y install --no-install-recommends git

RUN pip install --no-cache-dir uv

WORKDIR /workspace

# RUN uv init .
# RUN uv sync --no-cache