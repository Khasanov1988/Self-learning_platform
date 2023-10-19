FROM python:3

WORKDIR /code

COPY ./requirements.txt /code/

RUN pip install -r /code/requirements.txt && python3 manage.py csu && python3 manage.py renew_data_bases

COPY . .
