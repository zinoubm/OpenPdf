FROM node:18-alpine

WORKDIR /app

EXPOSE 5173


COPY public/ /app/public
COPY src/ /app/src
COPY package.json /app/

# RUN npm install

CMD ["npm", "run", "dev"]