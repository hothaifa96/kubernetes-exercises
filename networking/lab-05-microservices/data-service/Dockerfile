FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV AUTH_SECRET_KEY=default-secret-key-change-in-production

EXPOSE 5002

CMD ["python", "app.py"]
