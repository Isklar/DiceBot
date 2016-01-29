import discord
from discord.ext import commands
import random
import options
import string

username = options.username
password = options.password

client = discord.Client()
client.login(username, password)


# Connection confirmation
@client.event
async def on_ready():
    print('Connected!')
    print('Username: ' + client.user.name)
    print('ID: ' + client.user.id)
    print("------------------")
    

async def delete_messages(message):
    async for historicMessage in client.logs_from(message.channel):
        if historicMessage.author == client.user:
            await client.delete_message(historicMessage)
            
        if historicMessage.content.startswith('.r'):
            try:
               await client.delete_message(historicMessage)
            except:
               print('Error: Cannot delete messages!')  
  
async def roll(message, single=True):

    resultTotal = 0
    resultString = ''
    
    if single:
        dice = '1d20'
    else:
        dice = message.content[3:] #strip .r
        
    numDice = dice.split('d')[0]
    diceVal = dice.split('d')[1]
    await client.send_message(message.channel, "Rolling %s d%s" % (numDice, diceVal))
    
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await client.send_message(message.channel, 'Format has to be in xdx!')
        return
        
    for r in range(rolls):
        number = random.randint(1, limit)
        resultTotal = resultTotal + number
        
        if resultString == '':
            resultString += str(number)
        else:
            resultString += ', ' + str(number)

    await client.send_message(message.channel, message.author.mention + "  :game_die:\n**Result:** " + resultString + "\n**Total:** " + str(resultTotal))
    
@client.event
async def on_message(message):
    if message.author.id != client.user.id:
        if message.content.startswith('.r'):
            command = message.content[3:]
            
            if not command:
                await delete_messages(message)
                await roll(message)
            
            elif command != 'help':
                await delete_messages(message)
                await roll(message, False)
            
            else:
                await client.send_message(message.channel, "Usage: .r xdx")
                await client.send_message(message.channel, "e.g. `.r 3d20`")
        
client.run(username, password)