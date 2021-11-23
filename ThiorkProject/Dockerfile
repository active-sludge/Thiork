# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /ThiorkProject
COPY requirements.txt /ThiorkProject/
RUN pip install -r requirements.txt
COPY . /ThiorkProject/