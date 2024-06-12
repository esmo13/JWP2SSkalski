FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN apt update
RUN apt install -y libpq-dev gcc
RUN pip install -r requirements.txt 

CMD ["python3", "app.py"]