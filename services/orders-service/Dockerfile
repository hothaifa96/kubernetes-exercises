FROM node:20-alpine

WORKDIR /app

COPY package.json .

COPY . .

ENV SERVICE_NAME=orders-service \
    PORT=3002

EXPOSE 3002

CMD ["node", "index.js"]
