FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
RUN pip install Django==2.2.4
RUN pip install requests
COPY ./ /app/
WORKDIR /app/statfive
RUN python manage.py migrate
