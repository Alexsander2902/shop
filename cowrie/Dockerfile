# This Dockerfile contains two images, `builder` and `runtime`.
# `builder` contains all necessary code to build
# `runtime` is stripped down.

ARG ARCH=
ARG BUILD_DATE
FROM ${ARCH}debian:bullseye-slim as builder

WORKDIR /

# This is a temporary workaround, see https://github.com/cowrie/docker-cowrie/issues/26
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

ENV COWRIE_GROUP=cowrie \
    COWRIE_USER=cowrie \
    COWRIE_HOME=/cowrie

# Set locale to UTF-8, otherwise upstream libraries have bytes/string conversion issues
ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

RUN groupadd -r ${COWRIE_GROUP} && \
    useradd -r -d ${COWRIE_HOME} -m -g ${COWRIE_GROUP} ${COWRIE_USER}

# Set up Debian prereqs
RUN export DEBIAN_FRONTEND=noninteractive; \
    apt-get update && \
    apt-get install -y \
        -o APT::Install-Suggests=false \
        -o APT::Install-Recommends=false \
      python3-pip \
      ca-certificates \
      libffi-dev \
      libssl-dev \
      python3-dev \
      python3-venv \
      python3 \
      rustc \
      cargo \
      git \
      build-essential \
      python3-virtualenv \
      libsnappy-dev && \
    rm -rf /var/lib/apt/lists/*

# Build a cowrie environment from github master HEAD.

USER ${COWRIE_USER}

WORKDIR ${COWRIE_HOME}

RUN git clone --separate-git-dir=/tmp/cowrie.git https://github.com/cowrie/cowrie ${COWRIE_HOME}/cowrie-git && \
      python3 -m venv cowrie-env && \
      . cowrie-env/bin/activate && \
      pip install --no-cache-dir --upgrade pip wheel setuptools && \
      pip install --no-cache-dir --upgrade cffi && \
      pip install --no-cache-dir --upgrade -r ${COWRIE_HOME}/cowrie-git/requirements.txt && \
      pip install --no-cache-dir --upgrade -r ${COWRIE_HOME}/cowrie-git/requirements-output.txt

FROM ${ARCH}debian:bullseye-slim AS runtime

LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.authors="Michel Oosterhof <michel@oosterhof.net>"
LABEL org.opencontainers.image.url="https://cowrie.org/"
LABEL org.opencontainers.image.documentation="https://cowrie.readthedocs.io"
LABEL org.opencontainers.image.source="https://github.com/cowrie/docker-cowrie"
LABEL org.opencontainers.image.version="version"
LABEL org.opencontainers.image.revision="Source control revision identifier for the packaged software."
LABEL org.opencontainers.image.vendor="Cowrie"
LABEL org.opencontainers.image.licenses="BSD-3-Clause"
LABEL org.opencontainers.image.ref.name="latest"
LABEL org.opencontainers.image.title="Cowrie SSH/Telnet Honeypot"
LABEL org.opencontainers.image.description="Cowrie SSH/Telnet Honeypot"
LABEL org.opencontainers.image.base.digest="7beb0248fd81"
LABEL org.opencontainers.image.base.name="docker.io/library/debian:bullseye-slim"

ENV COWRIE_GROUP=cowrie \
    COWRIE_USER=cowrie \
    COWRIE_HOME=/cowrie

RUN groupadd -r ${COWRIE_GROUP} && \
    useradd -r -d ${COWRIE_HOME} -m -g ${COWRIE_GROUP} ${COWRIE_USER}

RUN export DEBIAN_FRONTEND=noninteractive; \
    apt-get update && \
    apt-get install -y \
        -o APT::Install-Suggests=false \
        -o APT::Install-Recommends=false \
      libssl1.1 \
      ca-certificates \
      libffi7 \
      procps \
      python3 \
      python3-distutils && \
    rm -rf /var/lib/apt/lists/* && \
    ln -s /usr/bin/python3 /usr/local/bin/python

COPY --from=builder --chown=${COWRIE_USER}:${COWRIE_GROUP} ${COWRIE_HOME} ${COWRIE_HOME}

ENV PATH=${COWRIE_HOME}/cowrie-git/bin:${PATH}
ENV COWRIE_STDOUT=yes

USER ${COWRIE_USER}
WORKDIR ${COWRIE_HOME}/cowrie-git

# preserve .dist file when etc/ volume is mounted
RUN cp ${COWRIE_HOME}/cowrie-git/etc/cowrie.cfg.dist ${COWRIE_HOME}/cowrie-git
VOLUME [ "/cowrie/cowrie-git/var", "/cowrie/cowrie-git/etc" ]
RUN mv ${COWRIE_HOME}/cowrie-git/cowrie.cfg.dist ${COWRIE_HOME}/cowrie-git/etc

#####RUN curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.14.1-amd64.deb && \
#####    dpkg -i filebeat-7.13.0-amd64.deb
#####
#####COPY filebeat.yml /etc/filebeat/filebeat.yml
#####COPY entrypoint.sh /entrypoint.sh
#####RUN chmod +x /entrypoint.sh
#####ENTRYPOINT [ "/entrypoint.sh" ]

ENTRYPOINT [ "cowrie" ]
CMD [ "start", "-n" ]
EXPOSE 2222 2223
