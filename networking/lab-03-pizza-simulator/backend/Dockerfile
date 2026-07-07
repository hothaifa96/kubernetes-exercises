FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV POD_NAME=local-pod
ENV POD_IP=127.0.0.1
ENV MONGO_URI=mongodb://localhost:27017
ENV DB_NAME=pizzadb

EXPOSE 5000

CMD ["python", "app.py"]
