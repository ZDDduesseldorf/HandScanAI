FROM node:latest

WORKDIR /frontend

COPY package.json ./

RUN npm install

COPY . .

RUN chmod +x docker-entrypoint.sh

ENTRYPOINT [ "sh", "./docker-entrypoint.sh" ]

EXPOSE 5173