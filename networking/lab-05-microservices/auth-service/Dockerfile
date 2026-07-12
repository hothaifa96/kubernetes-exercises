FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV AUTH_SECRET_KEY=default-secret-key-change-in-production
ENV AUTH_USER=admin
ENV AUTH_PASSWORD=secret
ENV TOKEN_EXPIRY_HOURS=24

EXPOSE 5001

CMD ["python", "app.py"]
