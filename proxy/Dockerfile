FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci --omit=dev

COPY . .

ENV NODE_END=production \
    PROXY_PORT=3000

USER node

EXPOSE 3000

CMD ["node", "app.js"]
