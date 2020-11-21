FROM python:3.8.1-slim-buster

# set work directory
ENV APPPATH=/app
WORKDIR ${APPPATH}

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt ${APPPATH}/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . ${APPPATH}
