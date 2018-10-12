FROM tiangolo/uwsgi-nginx-flask:python3.6

MAINTAINER Les1ie me@les1ie.com
WORKDIR /app

ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple
