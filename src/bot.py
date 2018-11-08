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
    # continue if message is in the polling channel
    if message.channel.name != 'polls':
        return
    
    # continue if the bot did not send this message
    if message.author == bot.user:
        return
    
    # mention the poll creater
    response = message.author.mention + ' created a poll!\n'

    # clean up the input
    content = message.content.replace('\n', '').split(';')
    for i in range(len(content)):
        content[i] = content[i].strip()
        if content[i] == '':
            del content[i]
    
    # must have a question and at least 2 options, discord sets a limit of 20 options
    if len(content) < 3 | len(content) > 21:
        return
    
    # separate question from options
    question = content[0]
    options = content[1:]

    # add the question to the response
    response += question + '\n;\n'
    
    # add all the options to the response
    for i in range(len(options)):
        response = ''.join([response, emojis[i], ' ', options[i], '\npercent\ngraph\n;\n'])
    
    # send the response
    poll = await bot.send_message(message.channel, response)
    
    # delete the post after the poll is made, this should force new name bubble every time
    await bot.delete_message(message)

    # react will all the options to the message we just sent
    for i in range(len(options)):
        await bot.add_reaction(poll, emojis[i])

def compute_graph(percent, length):
    num_bars = int(percent * length)
    return ''.join(['<', ''.join(['=' for _ in range(num_bars)]), ''.join(['_' for _ in range(length - num_bars)]), '>'])


async def on_reaction(reaction, user):
    # get the message that was reacted on
    message = reaction.message

    # continue if message is in polling channel
    if message.channel.name != 'polls':
        return
    
    # continue if message was sent by bot
    if message.author != bot.user:
       return

    # return if the bot reacted
    if user == bot.user:
        return

    # get total reaction count
    total_reactions = 0
    for react in message.reactions:
        total_reactions += react.count - 1

    if total_reactions < 0:
        return

    content = message.content.split('\n;\n')
    for i in range(1, len(content)):
        sections = content[i].split('\n')
        sections[1] = ''.join(['```', str(.33 * 100), '%'])
        sections[2] = ''.join([compute_graph(.33, 50), '```'])
        content[i] = '\n'.join(sections)
    result = '\n;\n'.join(content)
    print(result)
    await bot.edit_message(message, result)


@bot.event
async def on_reaction_add(reaction, user):
    await on_reaction(reaction, user)


@bot.event
async def on_reaction_remove(reaction, user):
    await on_reaction(reaction, user)


@bot.event
async def on_ready():
    print('Ready...')


bot.run(TOKEN)
