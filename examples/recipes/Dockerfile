FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

ADD requirements/production.txt /code/
ADD requirements/test.txt /code/

RUN pip install -U --no-cache-dir pip setuptools
RUN pip install --no-cache-dir -r test.txt
RUN ln -sf docker.env .env

ADD recipes /code/

ENTRYPOINT python -m recipes runserver
