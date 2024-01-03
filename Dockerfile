FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade -r /code/requirements.txt

COPY ./src/app /code/src/app
ENV PYTHONPATH=/code/src:/code/src/app

WORKDIR /code/src

CMD uvicorn app.main:app --host $APP_HOST --port $APP_PORT