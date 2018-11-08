import discord

TOKEN = ''

emojis = ["\N{REGIONAL INDICATOR SYMBOL LETTER A}", "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
          "\N{REGIONAL INDICATOR SYMBOL LETTER C}", "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
          "\N{REGIONAL INDICATOR SYMBOL LETTER E}", "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
          "\N{REGIONAL INDICATOR SYMBOL LETTER G}", "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
          "\N{REGIONAL INDICATOR SYMBOL LETTER I}", "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
          "\N{REGIONAL INDICATOR SYMBOL LETTER K}", "\N{REGIONAL INDICATOR SYMBOL LETTER L}",
          "\N{REGIONAL INDICATOR SYMBOL LETTER M}", "\N{REGIONAL INDICATOR SYMBOL LETTER N}",
          "\N{REGIONAL INDICATOR SYMBOL LETTER O}", "\N{REGIONAL INDICATOR SYMBOL LETTER P}",
          "\N{REGIONAL INDICATOR SYMBOL LETTER Q}", "\N{REGIONAL INDICATOR SYMBOL LETTER R}",
          "\N{REGIONAL INDICATOR SYMBOL LETTER S}", "\N{REGIONAL INDICATOR SYMBOL LETTER T}",
          "\N{REGIONAL INDICATOR SYMBOL LETTER U}", "\N{REGIONAL INDICATOR SYMBOL LETTER V}",
          "\N{REGIONAL INDICATOR SYMBOL LETTER W}", "\N{REGIONAL INDICATOR SYMBOL LETTER X}",
          "\N{REGIONAL INDICATOR SYMBOL LETTER Y}", "\N{REGIONAL INDICATOR SYMBOL LETTER Z}"]

bot = discord.Client()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.name == 'polls':
        await bot.delete_message(message)


    if message.content.startswith('/poll'):
        response = message.author.name + ' asked:\n'
        content = message.content.split(';')
        for i in range(len(content)):
            content[i] = content[i].strip()
        
        if len(content) < 3 | len(content) > 22:
            return
        
        question = content[1]
        options = content[2:]

        response += question + '\n'
        
        for i in range(len(options)):
            response += emojis[i] + ' ' + options[i] + '\n'
        
        
        poll = await bot.send_message(message.channel, response)
        
        for i in range(len(options)):
            await bot.add_reaction(poll, emojis[i])
        


@bot.event
async def on_ready():
    print('Ready...')


bot.run(TOKEN)
