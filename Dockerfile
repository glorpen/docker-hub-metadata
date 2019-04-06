FROM alpine:3.9 as base

LABEL maintainer="Arkadiusz Dzięgiel <arkadiusz.dziegiel@glorpen.pl>"

RUN wget https://gitlab.com/ConorIA/alpine-pandoc/raw/master/conor@conr.ca-584aeee5.rsa.pub -O /etc/apk/keys/conor@conr.ca-584aeee5.rsa.pub \
    && echo https://conoria.gitlab.io/alpine-pandoc/ >> /etc/apk/repositories \
    && echo "@testing http://nl.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories

RUN apk update \
  && apk add py3-requests pandoc \
  && rm /var/cache/apk/*

ADD description_updater.py /usr/local/bin/docker-hub-metadata

ENTRYPOINT ["/usr/local/bin/docker-hub-metadata"]
