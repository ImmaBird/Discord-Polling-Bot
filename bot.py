import discord

TOKEN = ''

bot = discord.Client()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('/poll'):
        await bot.delete_message(message)

        response = message.author.name + ' asked:\n'
        content = message.content.split(';')
        for i in range(len(content)):
            content[i] = content[i].strip()
        
        if len(content) < 3:
            return
        
        question = content[1]
        options = content[2:]

        response += question + '\n'

        letter = 'a'
        for i in range(len(options)):
            response += ':' + letter + ': ' + options[i] + '\n'
            letter = chr(ord(letter) + 1)
        
        
        poll = await bot.send_message(message.channel, response)

        letters = ['🄰', '🄱']
        print(letters)
        for i in range(len(options)):
            await bot.add_reaction(poll, letters[i])
            letter = chr(ord(letter) + 1)
        


@bot.event
async def on_ready():
    print('Ready...')
    letters = ['🄰', '🄱']
    print(letters)


bot.run(TOKEN)
