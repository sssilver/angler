FROM debian:latest

MAINTAINER sssilver@gmail.com

RUN apt-get update
RUN apt-get install -y build-essential git curl lsb-release libffi-dev locales-all
RUN apt-get install -y python python-dev python-setuptools python-software-properties python-pip
RUN apt-get install -y nginx supervisor libpq-dev

# Install Javascript goodies
RUN curl -sL https://deb.nodesource.com/setup | bash -
RUN apt-get update
RUN apt-get install -y nodejs
RUN npm install -g npm

# Configure nginx
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Upgrade pip
RUN pip install -U pip

RUN pip install uwsgi

# Deploy the code
RUN mkdir /opt/angler
ADD hook /opt/angler/hook
ADD rod /opt/angler/rod

# Install Hook dependencies
WORKDIR /opt/angler/hook
RUN npm install

# Install Rod
WORKDIR /opt/angler/rod
RUN python setup.py install

# Setup nginx site
RUN rm /etc/nginx/sites-enabled/*
ADD deploy/nginx/angler /etc/nginx/sites-enabled/angler

# Setup supervisord
ADD deploy/supervisor/angler.conf /etc/supervisor/conf.d/angler.conf

EXPOSE 80 8080

ENV PYTHONPATH /opt/angler/rod

CMD ["supervisord", "-n"]
