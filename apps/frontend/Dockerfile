FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm i 
COPY . .
EXPOSE 80
CMD ["node", "server.js"]
