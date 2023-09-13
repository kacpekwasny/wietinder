# Container for build frontend
FROM node:16-slim as nodeBuilder

WORKDIR /app
RUN mkdir frontend
COPY frontend/package.json ./frontend

ARG NODE_ENV
WORKDIR /app/frontend
RUN npm install

# RUN if [ "$NODE_ENV" = "development" ]; \
#         then npm install; \
#     else npm install --only=production; \
# fi
RUN apt-get update
RUN apt-get install tree

ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache
RUN tree /app -a -I 'node_modules|dist'
COPY ./frontend .

WORKDIR /app
COPY ./.env.production ./

RUN tree /app -a -I 'node_modules|dist'

WORKDIR /app/frontend
RUN npx vite build




# Conda Run Container
FROM continuumio/anaconda3


# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# ARG DEBIAN_FRONTEND=noninteractive
ENV TZ="Europe/Warsaw"

# RUN apt-get install -y tzdata locales
# RUN ln -fs /usr/share/zoneinfo/Europe/Warsaw /etc/localtime
# RUN echo "pl_PL.UTF-8 UTF-8" > /etc/locale.gen
# RUN locale-gen

# RUN apt-get install nano git procps cron -y
# RUN apt-get install libpq-dev python-dev gcc -y

WORKDIR /app

RUN pwd
RUN ls -la
COPY ./condaenv_ubuntu.yml .
RUN conda env create -f condaenv_ubuntu.yml

# Fron now on all commands will be run from `wietinder` environment
SHELL ["conda", "run", "-n", "wietinder", "/bin/bash", "-c"]


RUN mkdir frontend/
COPY --from=nodeBuilder /app/frontend/dist  ./frontend/dist

COPY ./backend  ./backend

ENV IS_PROD=true
WORKDIR /app/backend

RUN apt-get update
RUN apt-get install tree
RUN tree /app

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "wietinder",  "gunicorn", "main", "--bind", "0.0.0.0:8081", "--worker-class", "eventlet", "-w", "1", "--log-level", "debug" ]


# conda run --no-capture-output -n wietinder  gunicorn main --bind 0.0.0.0:8082 --worker-class eventlet -w 1 --log-level debug

