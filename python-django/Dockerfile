FROM python:3.8.3

ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN apt-get install nano

WORKDIR /usr/src/app

COPY docker-entrypoint.py /

EXPOSE 80

ENTRYPOINT ["python", "/docker-entrypoint.py"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]

