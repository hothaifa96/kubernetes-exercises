FROM node:20-alpine

WORKDIR /app

COPY package.json .

COPY . .

ENV PORT=3000 \
    order_URL=http://order-service:3001 \
    ORDERS_URL=http://orders-service:3002 \
    PRODUCTS_URL=http://products-service:3003

EXPOSE 3000

CMD ["node", "index.js"]
