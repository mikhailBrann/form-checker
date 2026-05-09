FROM python:3.11-alpine
RUN apk add --no-cache bash

# copy project
COPY ./app ./app
COPY ./shared/models ./app/models
# set work directory
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt