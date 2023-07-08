FROM python:3.9.7-slim-buster

# Path: /app

WORKDIR /app

# Path: /app/requirements.txt


COPY requirements.txt requirements.txt

# Path: /app

RUN pip3 install -r requirements.txt

# Path: /app

COPY . .

# gunicorn main:app -k main.GunicornAiohttpWorker -b 0.0.0.0:8080 --reload

CMD ["gunicorn", "main:app", "-k", "main.GunicornAiohttpWorker", "-b", "0.0.0.0:8080", "--reload"]