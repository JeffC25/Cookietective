FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y
RUN apt-get install python3 python3-pip ipython3 wget -y
RUN apt-get install firefox -y
RUN apt-get install sqlite3 -y
RUN apt-get install libpcap0.8 -y
RUN apt-get install mitmproxy -y

WORKDIR /home/Cookietective

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY Dockerfile .
COPY database.db .
COPY crawler/ ./crawler
COPY traffic_parser/ ./traffic_parser
COPY sql/ ./sql
COPY sample_urls.txt .
COPY cookie.sh .
COPY mitmproxy-ca-cert.crt .

RUN sqlite3 database.db "delete from cnamepackets" ".exit"
RUN sqlite3 database.db "delete from cookie" ".exit"
RUN sqlite3 database.db "delete from ip" ".exit"

ENTRYPOINT ["bash", "cookie.sh"]
