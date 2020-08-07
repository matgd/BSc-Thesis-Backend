FROM python:3.7-slim

ENV PYTHONBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=soonmeet_api.settings
ENV DEBUG=0

RUN mkdir soonmeet_api

COPY /soonmeet_api /soonmeet_api

RUN pip install -r /soonmeet_api/requirements.txt

EXPOSE 8000
CMD [ "python3", "/soonmeet_api/manage.py", "runserver", "0.0.0.0:8000" ] 
