# DiceBot
D&D Dice rolling bot for discord written in python.

## Requirements
This bot uses the [discord.py API wrapper](https://github.com/Rapptz/discord.py), you'll need to set that up for this bot to work.

Create a bot account using the [discord developer section](https://discordapp.com/developers/applications/me)

## Usage
Add your bot token in `options.py`

Add the bot to your server using the OAUTH url:
https://discordapp.com/oauth2/authorize?client_id=BOTCLIENTIDHERE&scope=bot&permissions=0x00002000

:exclamation: Make sure to insert your bots client ID in the url.

Start the bot using `python dbot.py` or by running RunLoop.bat

Roll dice using `.r 2d20`

If you give the bot permissions to manage messages on your server it will delete and previous rolls from the same user to avoid cluttering up chat.

### Extra bits
Thanks to Rapptz for the discord.py wrapper.

If you want any customization done to this bot for your own use feel free to join my [testing server](https://discord.gg/0n4QSS0mmQNtD5Ve) and message me

