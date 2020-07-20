FROM node:12.18

ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN apt-get install nano

RUN npm install -g @angular/cli@8.3.17

WORKDIR /usr/src/app

COPY docker-entrypoint.py /

EXPOSE 4200

ENTRYPOINT ["python3", "/docker-entrypoint.py"]

CMD ["ng", "serve", "--host", "0.0.0.0"]

