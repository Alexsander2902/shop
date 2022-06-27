FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
COPY . /python
WORKDIR /python
RUN pip install mysql-connector-python
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["main.py"]