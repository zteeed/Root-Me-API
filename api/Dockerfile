FROM tiangolo/uwsgi-nginx-flask:python3.7-alpine3.8

COPY ./requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY main.py /app/main.py
COPY api /app/api
