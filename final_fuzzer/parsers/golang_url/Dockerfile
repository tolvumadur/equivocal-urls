#Download base image ubuntu 20.04
FROM ubuntu:20.04

# LABEL about the custom image
LABEL maintainer="joshuar3@illinois.edu"
LABEL version="0.1"
LABEL description="This is the Docker Image for \
the golang-url parser."

# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive

RUN apt update

EXPOSE 8080