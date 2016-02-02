import discord
from discord.ext import commands
import random
import options
import string


description = '''D&D Dice rolling bot.'''
bot = commands.Bot(command_prefix='.', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.MissingRequiredArgument):
        await bot.send_message(ctx.message.author, 'Incorrect usage. Usage: .r XdX | .r 5d20')
    

async def delete_messages(message, author):
    async for historicMessage in bot.logs_from(message.channel):
        if historicMessage.author == bot.user:
            if (author.name in historicMessage.content) or (author.mention in historicMessage.content):
                await bot.delete_message(historicMessage)
            
        if historicMessage.content.startswith('.r'):
            if author == historicMessage.author:
                try:
                   await bot.delete_message(historicMessage)
                except:
                   print('Error: Cannot delete message!')  


@bot.command(pass_context=True)
async def r(ctx, dice : str):
    """Rolls a dice using XdX format.
    e.g .r 3d6"""
    
    resultTotal = 0
    resultString = ''
    
    try: 
        numDice = dice.split('d')[0]
        diceVal = dice.split('d')[1]
    except Exception:
        await bot.say("Format has to be in xdx %s." % ctx.message.author)
        return

    if int(numDice) > 500:
        await bot.say("I cant roll that many dice %s." % ctx.message.author)
        return

    await delete_messages(ctx.message, ctx.message.author)
    
    bot.type()
    await bot.say("Rolling %s d%s for %s" % (numDice, diceVal, ctx.message.author))
    rolls, limit = map(int, dice.split('d'))

    for r in range(rolls):
        number = random.randint(1, limit)
        resultTotal = resultTotal + number
        
        if resultString == '':
            resultString += str(number)
        else:
            resultString += ', ' + str(number)
    
    if numDice == '1':
        await bot.say(ctx.message.author.mention + "  :game_die:\n**Result:** " + resultString + "\n─────────────────────────")
    else:
        await bot.say(ctx.message.author.mention + "  :game_die:\n**Result:** " + resultString + "\n**Total:** " + str(resultTotal) + "\n─────────────────────────")


bot.run(options.username, options.password)