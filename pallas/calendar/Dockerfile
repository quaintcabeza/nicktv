FROM python:3.9.1-slim-buster

ENV GROUP_ID=1000 \
    USER_ID=1000

RUN apt-get update
RUN apt-get install --yes cron

WORKDIR /var/calendar/

COPY requirements.txt /var/calendar/
RUN pip install -r /var/calendar/requirements.txt

COPY sync.py /var/calendar/sync.py
COPY start_cron.sh /var/calendar/start_cron.sh

CMD /var/calendar/start_cron.sh
