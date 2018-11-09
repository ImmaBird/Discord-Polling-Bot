FROM arm32v6/python:3.6

RUN [ "python", "-m", "pip", "install", "discord.py==0.16.12" ]

WORKDIR /discord-bot

COPY . /discord-bot

RUN [ "python", "-u", "bot.py" ]
