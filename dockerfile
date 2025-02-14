FROM python:3.12-slim

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app

ENTRYPOINT ["./docker_entrypoint.sh"]
