FROM debian:latest

MAINTAINER sssilver@gmail.com

RUN apt-get update
RUN apt-get install -y build-essential git curl lsb-release
RUN apt-get install -y python python-dev python-setuptools python-software-properties python-pip
RUN apt-get install -y nginx supervisor sqlite3

# Install Node.js and Javascript goodies
RUN curl -sL https://deb.nodesource.com/setup | bash -
RUN apt-get update
RUN apt-get install -y nodejs npm
RUN npm install -g bower

# Configure nginx
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Upgrade pip
RUN pip install -U pip

RUN pip install uwsgi

# Deploy the code
RUN mkdir /opt/angler
ADD hook /opt/angler/hook
ADD rod /opt/angler/rod

# Install dependencies
WORKDIR /opt/angler/hook
RUN bower install --allow-root
WORKDIR /opt/angler
RUN pip install -r rod/requirements.txt

# Setup nginx site
RUN rm /etc/nginx/sites-enabled/*
ADD deploy/nginx/angler /etc/nginx/sites-enabled/angler

# Setup supervisord
ADD deploy/supervisor/angler.conf /etc/supervisor/conf.d/angler.conf

EXPOSE 80 8080

RUN export PYTHONPATH=/opt/angler/rod

CMD ["supervisord", "-n"]
