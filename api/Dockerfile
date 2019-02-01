FROM python:3-alpine

EXPOSE 5000

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY main.py . 
COPY api/ ./api

CMD ["python", "main.py"]
