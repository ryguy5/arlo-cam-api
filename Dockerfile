FROM python:3.10-slim

WORKDIR /opt/arlo-cam-api
COPY . ./

RUN pip3 install -r requirements.txt

EXPOSE 4000/tcp
EXPOSE 4100/tcp
EXPOSE 5000/tcp

CMD python3 server.py
