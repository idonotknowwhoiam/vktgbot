FROM python:3.8-alpine
WORKDIR /code

COPY requirements.txt ./
RUN apk update &&\
    apk add --no-cache --virtual .build-deps \
    build-base \
    gcc &&\
    pip install --user -r requirements.txt &&\
    apk del .build-deps &&\
    rm -rf /root/* /tmp/*

COPY bot.py admin.py config.yaml ./

CMD [ "python", "./bot.py" ]

# todo: volumes, env vars, gitgub-docker-repo

