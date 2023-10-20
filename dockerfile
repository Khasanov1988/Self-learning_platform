FROM python:3

LABEL authors="Ilnar Khasanov"

WORKDIR /code

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .
