FROM python:3.7-alpine

COPY ./main.py /bot/
COPY ./contentHandler.py /bot/
COPY ./secret_constants.py /bot/

COPY requirements.txt /tmp

RUN apk --update add \
 build-base \
 jpeg-dev \
 zlib-dev

RUN pip3 install -r /tmp/requirements.txt

WORKDIR /bot

CMD ["python3", "main.py"]



