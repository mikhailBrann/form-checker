FROM python:3.11-alpine
RUN apk add --no-cache bash

# copy project
COPY ./app ./app
COPY ./shared/models ./app/models
# set work directory
WORKDIR /app

# # Скачиваем BMP (одной строкой с полной ссылкой)
# RUN wget https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.4/browsermob-proxy-2.1.4-bin.zip \
#     && unzip browsermob-proxy-2.1.4-bin.zip \
#     && rm browsermob-proxy-2.1.4-bin.zip

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt