FROM python:3.9-alpine

RUN pip install prometheus_client requests

ENV BIND_PORT 9187

ADD src /app
WORKDIR /app

CMD ["python", "mailjet_exporter.py"]
