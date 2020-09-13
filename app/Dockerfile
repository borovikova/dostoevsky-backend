# pull official base image
FROM python:3.8-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc && \
    apt-get clean

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN adduser user && addgroup app && adduser user app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/app
RUN mkdir $APP_HOME/app/static
WORKDIR $APP_HOME

# copy project
COPY . $APP_HOME

# copy entrypoint-prod.sh
COPY ./entrypoint.sh $APP_HOME

# chown all the files to the app user
RUN chown -R user:app $APP_HOME

# change to the app user
USER user

# run entrypoint.prod.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]