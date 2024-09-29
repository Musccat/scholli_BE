# # Pull the image from Dockerhub
# FROM python:alpine3.19

# # 필요한 패키지 설치
# RUN apk add --no-cache gcc musl-dev mariadb-dev pkgconfig

# WORKDIR /src

# # set up python environment variables

# ENV PYTHONDOWNWRITEBYTECODE 1
# ENV PYTHONNUNBUFFER 1

# # update and  install dependencies
# RUN pip install --upgrade pip
# COPY ./requirements.txt /api/requirements.txt
# RUN pip install -r /api/requirements.txt

# # copy project
# COPY . .

# # Expose the port server is running on
# EXPOSE 8000

FROM python:3.10.0-alpine
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

# dependencies for psycopg2-binary
RUN apk add --no-cache mariadb-connector-c-dev libffi-dev gcc musl-dev
RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app/