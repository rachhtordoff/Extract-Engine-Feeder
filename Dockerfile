FROM python:3.7
MAINTAINER Rachael Tordoff


COPY / /opt/

RUN pip3 install -q -r /opt/requirements.txt && \
  pip3 install -q -r /opt/requirements_test.txt

WORKDIR /opt

CMD ["python3", "run.py"]
