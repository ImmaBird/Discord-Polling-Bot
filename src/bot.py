import discord
import sys

TOKEN = sys.argv[1]

emoji_nums = {"\N{REGIONAL INDICATOR SYMBOL LETTER A}":0, "\N{REGIONAL INDICATOR SYMBOL LETTER B}":1,
          "\N{REGIONAL INDICATOR SYMBOL LETTER C}":2, "\N{REGIONAL INDICATOR SYMBOL LETTER D}":3,
          "\N{REGIONAL INDICATOR SYMBOL LETTER E}":4, "\N{REGIONAL INDICATOR SYMBOL LETTER F}":5,
          "\N{REGIONAL INDICATOR SYMBOL LETTER G}":6, "\N{REGIONAL INDICATOR SYMBOL LETTER H}":7,
          "\N{REGIONAL INDICATOR SYMBOL LETTER I}":8, "\N{REGIONAL INDICATOR SYMBOL LETTER J}":9,
          "\N{REGIONAL INDICATOR SYMBOL LETTER K}":10, "\N{REGIONAL INDICATOR SYMBOL LETTER L}":11,
          "\N{REGIONAL INDICATOR SYMBOL LETTER M}":12, "\N{REGIONAL INDICATOR SYMBOL LETTER N}":13,
          "\N{REGIONAL INDICATOR SYMBOL LETTER O}":14, "\N{REGIONAL INDICATOR SYMBOL LETTER P}":15,
          "\N{REGIONAL INDICATOR SYMBOL LETTER Q}":16, "\N{REGIONAL INDICATOR SYMBOL LETTER R}":17,
          "\N{REGIONAL INDICATOR SYMBOL LETTER S}":18, "\N{REGIONAL INDICATOR SYMBOL LETTER T}":19,
          "\N{REGIONAL INDICATOR SYMBOL LETTER U}":20, "\N{REGIONAL INDICATOR SYMBOL LETTER V}":21,
          "\N{REGIONAL INDICATOR SYMBOL LETTER W}":22, "\N{REGIONAL INDICATOR SYMBOL LETTER X}":23,
          "\N{REGIONAL INDICATOR SYMBOL LETTER Y}":24, "\N{REGIONAL INDICATOR SYMBOL LETTER Z}":25}

num_emojis = {v: k for k, v in emoji_nums.items()}

bot = discord.Client()


def compute_graph(percent, length):
    num_bars = int(percent * length)
    return ''.join(['<', ''.join(['=' for _ in range(num_bars)]), ''.join(['_' for _ in range(length - num_bars)]), '>'])


@bot.event
async def on_message(message):
    # continue if message is in the polling channel
    if message.channel.name != 'polls':
        return
    
    # continue if the bot did not send this message
    if message.author == bot.user:
        return
    
    # mention the poll creater
    response = message.author.mention + ' asked:\n'

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
        response = ''.join([response, num_emojis[i], ' ', options[i], '\n```0%\n', compute_graph(0, 50), '```\n;\n'])
    
    # send the response
    poll = await bot.send_message(message.channel, response)
    
    # delete the post after the poll is made, this should force new name bubble every time
    await bot.delete_message(message)

    # react will all the options to the message we just sent
    for i in range(len(options)):
        await bot.add_reaction(poll, num_emojis[i])


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
    for react in message.reactions:
        i = emoji_nums[str(react.emoji)] + 1
        percent = 0
        if total_reactions != 0:
            percent = (react.count - 1) / total_reactions
        sections = content[i].split('\n')
        sections[1] = ''.join(['```', str(percent * 100), '%'])
        sections[2] = ''.join([compute_graph(percent, 50), '```'])
        content[i] = '\n'.join(sections)
    result = '\n;\n'.join(content)
    await bot.edit_message(message, result)


@bot.event
async def on_reaction_add(reaction, user):
    await on_reaction(reaction, user)


@bot.event
async def on_reaction_remove(reaction, user):
    await on_reaction(reaction, user)


@bot.event
async def on_ready():
    # channel = discord.utils.get(bot.get_all_channels(), name='polls')
    # emoji = num_emojis[0]
    # async for log in bot.logs_from(channel, limit=100, reverse=True):
    #     if log.author == bot.user:
    #         await bot.edit_message(log, log.content)
    print('Ready...')


bot.run(TOKEN)
