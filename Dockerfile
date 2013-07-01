FROM ubuntu
MAINTAINER John Costa <john.costa@gmail.com>

RUN apt-get update
RUN apt-get install -y git python curl
RUN curl -O http://python-distribute.org/distribute_setup.py
RUN python distribute_setup.py
RUN easy_install pip
RUN pip install git+https://github.com/johncosta/docker-AMI
