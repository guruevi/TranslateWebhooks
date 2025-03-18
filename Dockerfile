FROM ubuntu:latest
LABEL authors="evanoost"

ENTRYPOINT ["top", "-b"]