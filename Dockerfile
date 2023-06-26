FROM python:3.11-slim-bullseye

WORKDIR /usr/src/app

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# ARG DEBIAN_FRONTEND=noninteractive

ENV TZ="Europe/Warsaw"

RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install -y tzdata locales

RUN ln -fs /usr/share/zoneinfo/Europe/Warsaw /etc/localtime

RUN echo "pl_PL.UTF-8 UTF-8" > /etc/locale.gen

RUN locale-gen

RUN apt-get install nano git procps cron -y
RUN apt-get install libpq-dev python-dev gcc -y

COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

COPY ./start.sh ./start.sh
RUN chmod +x start.sh

RUN echo "from app.app import create_app" > wsgi.py
RUN echo "application = create_app()" >> wsgi.py

