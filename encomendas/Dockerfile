FROM python:3.12-slim

WORKDIR /app

RUN pip install flask requests

COPY main.py .

EXPOSE 5000

CMD ["python", "main.py"]
