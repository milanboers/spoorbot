FROM python:alpine

RUN apk update && apk add build-base gcc git libffi-dev

RUN pip3 install pipenv
RUN mkdir -p /app/spoorbot

WORKDIR /app
COPY Pipfile Pipfile
RUN pipenv install

COPY spoorbot /app/spoorbot/

ENTRYPOINT ["pipenv", "run", "python", "-m", "spoorbot"]
