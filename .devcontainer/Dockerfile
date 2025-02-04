
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Install additional packages
RUN apt update && export DEBIAN_FRONTEND=noninteractive \
    && apt -y install --no-install-recommends git openjdk-17-jre

RUN pip install --no-cache-dir uv

RUN export JAVA_HOME=$(readlink -f $(which java)) >> ~/.bashrc && export PATH=$JAVA_HOME/bin:$PATH >> ~/.bashrc

WORKDIR /workspace

# RUN uv init .
# RUN uv sync --no-cache