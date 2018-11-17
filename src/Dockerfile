FROM python:3.6

RUN [ "python", "-m", "pip", "install", "discord.py==0.16.12" ]

WORKDIR /discord-bot

COPY bot.py .

ENTRYPOINT [ "python", "-u", "bot.py" ]
