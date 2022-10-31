FROM --platform=linux/amd64 python:3.9.14

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8

WORKDIR /odn_socket
COPY . /odn_socket

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN apt-get update && apt-get upgrade -y


ENTRYPOINT [ "python", "./socket_server.py" ]
