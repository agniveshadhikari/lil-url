FROM python:3.11.1-bullseye

COPY . /app/
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["uwsgi", "uwsgi/config.ini"]
