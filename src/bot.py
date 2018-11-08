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
    content = message.content.remove('\n').split(';')
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
    response += question + ' ;\n'
    
    # add all the options to the response
    for i in range(len(options)):
        response += emojis[i] + ' ' + options[i] + '\n```0%\n<                                                  >```;\n'
    
    # send the response
    poll = await bot.send_message(message.channel, response)
    
    # delete the post after the poll is made, this should force new name bubble every time
    await bot.delete_message(message)

    # react will all the options to the message we just sent
    for i in range(len(options)):
        await bot.add_reaction(poll, emojis[i])


def array_to_string(array):
    result = ''
    for element in array:
        result += element + '\n'
    return result


def on_reaction(reaction, user):
    # get the message that was reacted on
    message = reaction.message

    # continue if message is in polling channel
    if message.channel.name != 'polls':
        return

    # continue if message was sent by bot
    if message.author != bot.user:
        return

    # get total reaction count
    total_reactions = 0
    for react in message.reactions:
        total_reactions += react.count - 1
    
    # get percentage of votes
    percent_votes = reaction.count / total_reactions * 100

    content = message.content.split(';')
    emoji = reaction.emoji
    
    result = ''
    for i in range(1, len(content)):
        if content[i].startswith(emoji):
            options = content[i].split('\n')
            options[1] = '```' +  percent_votes + '%'
            options[2] = '<'
            for j in range(50):
                if j < percent_votes / 2:
                    options[2] += '='
                else:
                    options[2] += ' '
            options[2] += '>```;'
            content[i] = array_to_string(options)
            result = array_to_string(content)
            break
    
    await bot.edit_message(message, result)


@bot.event
async def on_reaction_add(reaction, user):
    on_reaction(reaction, user)


@bot.event
async def on_reaction_remove(reaction, user):
    on_reaction(reaction, user)


@bot.event
async def on_ready():
    print('Ready...')


bot.run(TOKEN)
