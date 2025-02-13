FROM python:3.10-alpine3.19

WORKDIR /usr/src/app

EXPOSE 8000

RUN pip install --upgrade pip

COPY requirements.txt /temp/requirements.txt
RUN pip install -r /temp/requirements.txt

COPY . .
