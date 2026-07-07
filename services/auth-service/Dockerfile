FROM node:20-alpine

WORKDIR /app

COPY package.json .

COPY . .

ENV SERVICE_NAME=order-service \
    PORT=3001

EXPOSE 3001

CMD ["node", "index.js"]
