FROM python:3.13-slim

# Update system packages to address vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Install git
RUN apt install -y git-all
    
# install sqlite
USER root
RUN apt-get -y update && \
    apt-get -y install sqlite3 libsqlite3-dev

RUN python -m pip install --upgrade pip

RUN mkdir -p /app/log  \
    && chown ${USERNAME}:${USERNAME} /app/log

# install app requirements
USER ${USERNAME}
WORKDIR /home/${USERNAME}

COPY requirements.txt /home/${USERNAME}
RUN python -m pip install -r /home/${USERNAME}/requirements.txt --no-cache-dir && \
    rm /home/${USERNAME}/requirements.txt
