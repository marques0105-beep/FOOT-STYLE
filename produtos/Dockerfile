FROM python:3.12-slim

WORKDIR /app

RUN pip install flask

COPY main.py .
COPY templates ./templates

EXPOSE 5000

CMD ["python", "main.py"]
