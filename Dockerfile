FROM python:3.9.7-slim-buster

# Path: /app

WORKDIR /app

# Path: /app/requirements.txt


COPY requirements.txt requirements.txt

# Path: /app

RUN pip3 install -r requirements.txt

# Path: /app

COPY . .


RUN ["chmod", "+x", "scripts/run.sh"]

# Path: /app

CMD ["/app/scripts/run.sh"]