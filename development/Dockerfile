
ARG python_ver=3.7
FROM python:${python_ver}

ENV PYTHONUNBUFFERED 1

RUN mkdir /prom_cache
ENV prometheus_multiproc_dir /prom_cache 

RUN mkdir -p /opt

RUN pip install --upgrade pip\
  && pip install poetry

# -------------------------------------------------------------------------------------
# Install Deployment Keys
# -------------------------------------------------------------------------------------
COPY ./development/ssh_config /source/development/ssh_config
COPY ./development/deployment_keys /source/development/deployment_keys
RUN mkdir /root/.ssh && \
    mv /source/development/ssh_config /root/.ssh/config && \
    mv /source/development/deployment_keys /root/.ssh && \
    chmod -R 600 /root/.ssh

# -------------------------------------------------------------------------------------
# Download Grimlock
# -------------------------------------------------------------------------------------
ARG GRIMLOCK_VERSION=${GRIMLOCK_VERSION}
ARG GRIMLOCK_HASH=${GRIMLOCK_HASH}
WORKDIR /opt
RUN git clone git@grimlock:networktocode-llc/grimlock.git --single-branch --branch $GRIMLOCK_VERSION
# Temporarily we are deploying from an integration branch of Grimlock, as there are no releases
# We still need to figure out what is deployed if there are issues so we change the version number
# here to include the short commit hash
RUN mv /opt/grimlock /opt/nautobot && cd /opt/nautobot && \
    git reset --hard $GRIMLOCK_HASH && \
    githash=$(git rev-parse --short HEAD) && \
    sed -i "s@^VERSION = \(.*\)'@VERSION = \1+$githash'@"  netbox/netbox/settings.py

# -------------------------------------------------------------------------------------
# Install Nautobot
# -------------------------------------------------------------------------------------
# ARG nautobot_ver=${NAUTOBOT_VER}
# RUN git clone --single-branch --branch ${nautobot_ver} https://github.com/nautobot-community/nautobot.git /opt/nautobot/ && \
RUN cd /opt/nautobot/ && \
    pip install -r /opt/nautobot/requirements.txt

# Make the django-debug-toolbar always visible when DEBUG is enabled,
# except when we're running Django unit-tests.
RUN echo "import sys" >> /opt/nautobot/netbox/netbox/settings.py && \
    echo "TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'" >> /opt/nautobot/netbox/netbox/settings.py && \
    echo "DEBUG_TOOLBAR_CONFIG = {'SHOW_TOOLBAR_CALLBACK': lambda _: DEBUG and not TESTING }" >> /opt/nautobot/netbox/netbox/settings.py

# -------------------------------------------------------------------------------------
# Install Nautobot Plugin
# -------------------------------------------------------------------------------------
RUN mkdir -p /source
WORKDIR /source
COPY . /source
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

WORKDIR /opt/nautobot/netbox/
