import discord
from discord.ext import commands
import random
import options
import string
import re


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
        await bot.send_message(ctx.message.channel, 'Usage: `.r #d#` e.g. `.r 1d20`\nUse .help for more info.')
    

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
                   print('Error: Cannot delete user message!')  


@bot.command(pass_context=True)
async def r(ctx, roll : str):
    """Rolls a dice using #d# format.
    e.g .r 3d6"""
    
    resultTotal = 0
    resultString = ''
    
    try: 
        numDice = roll.split('d')[0]
        diceVal = roll.split('d')[1]
    except Exception as e:
        print(e)
        await bot.say("Format has to be in #d# %s." % ctx.message.author.name)
        return

    if int(numDice) > 500:
        await bot.say("I cant roll that many dice %s." % ctx.message.author.name)
        return

    await delete_messages(ctx.message, ctx.message.author)
    
    bot.type()
    await bot.say("Rolling %s d%s for %s" % (numDice, diceVal, ctx.message.author.name))
    rolls, limit = map(int, dice.split('d'))

    for r in range(rolls):
        number = random.randint(1, limit)
        resultTotal = resultTotal + number
        
        if resultString == '':
            resultString += str(number)
        else:
            resultString += ', ' + str(number)
    
    if numDice == '1':
        await bot.say(ctx.message.author.mention + "  :game_die:\n**Result:** " + resultString)
    else:
        await bot.say(ctx.message.author.mention + "  :game_die:\n**Result:** " + resultString + "\n**Total:** " + str(resultTotal))

@bot.command(pass_context=True)
async def rt(ctx, roll : str):
    """Rolls dice using #d#s# format with a set success threshold, Where s is the thresold type (< = >).
    e.g .r 3d10<55"""

    numberSuccesses = 0
    resultString = ''
    
    try: 
        valueList = re.split("(\d+)", roll)
        valueList = list(filter(None, valueList))

        diceCount = int(valueList[0])
        diceValue = int(valueList[2])
        thresholdSign = valueList[3]
        successThreshold = int(valueList[4])

    except Exception as e:
        print(e)
        await bot.say("Format has to be in #d#t# %s." % ctx.message.author.name)
        return
    
    if int(diceCount) > 500:
        await bot.say("I cant roll that many dice %s." % ctx.message.author.name)
        return

    await delete_messages(ctx.message, ctx.message.author)

    bot.type()
    await bot.say("Rolling %s d%s for %s with a success theshold %s %s" % (diceCount, diceValue, ctx.message.author.name, thresholdSign, successThreshold))

    try:
        for r in range(0, diceCount):

            number = random.randint(1, diceValue)
            isRollSuccess = False
            
            if thresholdSign == '<':
                if number < successThreshold:
                    numberSuccesses += 1
                    isRollSuccess = True

            elif thresholdSign == '=':
                if number == successThreshold:
                    numberSuccesses += 1
                    isRollSuccess = True

            else: # >
                if number > successThreshold:
                    numberSuccesses += 1
                    isRollSuccess = True

            if resultString == '':
                if isRollSuccess:
                    resultString += '**' + str(number) + '**'
                else:
                    resultString += str(number)
            else:
                if isRollSuccess:
                    resultString += ', ' + '**' + str(number) + '**'
                else:
                    resultString += ', ' + str(number)

            isRollSuccess = False


        if diceCount == 1:
            if numberSuccesses == 0:
                await bot.say(ctx.message.author.mention + "  :game_die:\n**Result:** " + resultString + "\n**Success:** :x:" )
            else:
                await bot.say(ctx.message.author.mention + "  :game_die:\n**Result:** " + resultString + "\n**Success:** :white_check_mark:" )
        else:
            await bot.say(ctx.message.author.mention + "  :game_die:\n**Result:** " + resultString + "\n**Successes:** " + str(numberSuccesses))
    except Exception as e:
        print(e)
        return

bot.run(options.token)