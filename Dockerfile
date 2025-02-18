FROM python:3.10-slim-bullseye

COPY webhook.py .

RUN pip install feedparser discord requests

ENTRYPOINT ["python","webhook.py"]