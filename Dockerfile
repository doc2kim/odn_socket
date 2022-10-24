FROM --platform=linux/amd64 python:3.9.14

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8

WORKDIR /odn_socket

RUN pip install --upgrade pip

RUN apt-get update && apt-get upgrade -y

COPY requirements.txt /odn_api/

ADD . /odn_socket

RUN pip install -r requirements.txt
