FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        iputils-ping \
        dnsutils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ping-curl.sh .
RUN chmod +x ping-curl.sh

ENV TARGET=localhost

ENTRYPOINT ["/app/ping-curl.sh"]
