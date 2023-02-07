FROM python:3.11.1-bullseye

# Install requirements
COPY ./requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

# Copy the srcs
COPY . ./


ENTRYPOINT ["uwsgi", "uwsgi/config.ini"]
