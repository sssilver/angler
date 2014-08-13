FROM debian:latest

MAINTAINER sssilver@gmail.com

RUN apt-get update
RUN apt-get install -y build-essential git
RUN apt-get install -y python python-dev python-setuptools python-software-properties python-pip
RUN apt-get install -y nginx supervisor sqlite3

# Configure nginx
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Upgrade pip
RUN pip install -U pip

RUN pip install uwsgi

# Deploy the code
RUN mkdir /opt/angler
ADD . /opt/angler

WORKDIR /opt/angler
RUN pip install -r rod/requirements.txt

EXPOSE 80
CMD ["supervisord", "-n"]
