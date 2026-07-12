FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --omit=dev

COPY server.js .
COPY public/ ./public/

ENV PORT=3000
ENV AUTH_SERVICE_URL=http://auth-service:5001
ENV DATA_SERVICE_URL=http://data-service:5002
ENV FRONTEND_USER=admin
ENV FRONTEND_PASSWORD=secret

EXPOSE 3000

CMD ["npm", "start"]
