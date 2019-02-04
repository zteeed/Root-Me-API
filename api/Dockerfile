FROM python:3-alpine

EXPOSE 5000

ENV GUNICORN_WORKER_COUNT 4
ENV GUNICORN_PORT 5000

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

COPY main.py . 
COPY api/ ./api

CMD ["sh", "-c", "gunicorn -w $GUNICORN_WORKER_COUNT -b 0.0.0.0:$GUNICORN_PORT main:app"]
