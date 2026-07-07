FROM node:20-alpine

WORKDIR /app

COPY package.json .

COPY . .

ENV SERVICE_NAME=products-service \
    PORT=3003

EXPOSE 3003

CMD ["node", "index.js"]
