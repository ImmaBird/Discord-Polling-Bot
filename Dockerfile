FROM node

COPY . /discord-bot

WORKDIR /discord-bot

RUN [ "node", "bot.js" ]
