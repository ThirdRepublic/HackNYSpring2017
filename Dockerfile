FROM python:2.7

ADD ./ /opt/
WORKDIR /opt/
RUN apt-get update && apt-get install -y python-dev python-pip && pip install -r requirements.txt
CMD python serve.py
