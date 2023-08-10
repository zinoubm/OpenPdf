FROM node:18-alpine

WORKDIR /app

EXPOSE 3000


COPY public/ /app/public
COPY src/ /app/src
COPY package.json /app/

# RUN npm install

CMD ["npm", "start"]