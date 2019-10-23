FROM silencezhao90/contos-python36:v1

MAINTAINER <silencezhao_90@163.com>

ENV TZ "Asia/Shanghai"

RUN yum -y install libxml2* libpq-dev postgresql-devel

COPY requirements.txt /home/deploy/
WORKDIR /home/deploy/gree
RUN pip3 install --upgrade pip \
    &&pip3 install -r /home/deploy/requirements.txt

EXPOSE 8000

STOPSIGNAL SIGTERM