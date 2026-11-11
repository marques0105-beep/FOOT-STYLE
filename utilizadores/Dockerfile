FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install 

COPY main.py .

EXPOSE 5000

CMD ["python", "main.py"]
