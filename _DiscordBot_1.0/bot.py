# bot.py
import os
import discord
import random
import pytz
import datetime
import scrapeGame
import game
import cdkey
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CommandInvokeError, BadArgument
from pytz import timezone
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()
bot = commands.Bot(command_prefix='!', help_command=None)

val_channels=[]
sen_channels=['bot-dev']

server_mainID = #server ID
bot_dev1 = #dev channel ID
bot_dev2 = #dev channel ID
log_chanID = #logging channel ID


# Normal Functions
def logChan():
    log_channel = bot.get_channel(log_chanID)
    return log_channel

# Bot Commands
@bot.command(name='hello', help='Bot responds with a salutation.')
async def hello(ctx):
    salutations = [
        'Hello!',
        'Um, hi?',
        'Stop bothering me!'
    ]
    response = random.choice(salutations)
    await ctx.send(response)

@bot.command(name='rolldice', help='Simulates rolling dice')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

@bot.command(name='coinflip', help='Simulates flipping a coin')
async def flip(ctx):
    faces = [
        'heads',
        'tails'
    ]
    response = random.choice(faces)
    await ctx.send(response)

@bot.command(name='gcid', help='Gets channel ID info')
@has_permissions(administrator=True)
async def getcid(ctx):
    cid = ctx.message.channel.id
    msg = f'channel:{cid} | serverid:{ctx.message.guild.id}'
    await ctx.send(msg)

@bot.command(name='ca', pass_context = True)
@has_permissions(administrator=True)
async def whoami(ctx):
    if ctx.message.channel.name in sen_channels:
        msg = f'You are an admin {ctx.message.author.name} and asked in {ctx.message.channel.name}'
        await ctx.send(msg)

@bot.command(name='tz', help='Gets current time from timezones.')
async def tz(ctx):
    fmt = '%m/%d %H:%M'
    pt = pytz.timezone("US/Pacific")
    et = pytz.timezone("US/Eastern")
    uk = pytz.timezone("Europe/London")
    my_ct = datetime.datetime.now(tz=pytz.UTC)
    dt_pt = f'{(my_ct.astimezone(pt)).strftime(fmt)} - Pacific'
    dt_et = f'{(my_ct.astimezone(et)).strftime(fmt)} - Eastern'
    dt_uk = f'{(my_ct.astimezone(uk)).strftime(fmt)} - GMT+1'
    times = [dt_pt, dt_et, dt_uk]
    await ctx.send('\n'.join(times))

@bot.command(name='ss', help='Scrapes steam and other sites based on URL')
async def ss(ctx, url):
    rgame = scrapeGame.parseSteamURL(url)
    cdgame = scrapeGame.lookUpCDKeys(rgame.url)

    # Embedded message for information on Steam game
    steamhl = "[Steam Page]({})".format(rgame.url)

    msg = discord.Embed(title=rgame.title,
                        description=rgame.description,
                        color=0x4a83a6)
    msg.add_field(name='Sentiment', value=rgame.sentiment, inline=True)
    msg.add_field(name='Genre', value=rgame.genre, inline=True)
    msg.add_field(name='Features', value=', '.join(rgame.features), inline=False)
    msg.add_field(name='Steam Options', value=steamhl + '\n~' + '\n~'.join(rgame.purchases) + '\n ', inline=False)
    #msg.add_field(name="\u200b", value="\u200b", inline=False)
    msg.add_field(name='\nCdkeys', value="Results are broadly searched and may be inaccurate.", inline=False)
    # Cdkey additional lookups
    for x in cdgame:
        hlurl = "[{}]({})".format(x.title, x.url)
        b_entry = f'~{x.title} | {x.region} | {x.platform} | {x.price} | {x.availability}'
        g_entry = hlurl + f'```yaml\n{x.region} | {x.platform} | Price: {x.price} | {x.availability}\n\n```'
        if rgame.title in x.title:
            if "In stock" in x.availability:
                msg.add_field(name="\u200b", value=g_entry, inline=False)
            else:
                msg.add_field(name="\u200b", value=b_entry, inline=False)

    await ctx.send(embed=msg)


@bot.command(name='help', help='Gets info on all commands.')
async def helpMe(ctx):
    commands = {}
    commands['!ss <steam url>'] = 'Gets information about game and looks up other sites based on Steam URL.'
    commands['!tz'] = 'Gets current time from timezones.'
    commands['!coinflip'] = 'Simulates flipping a coin.'
    commands['!rolldice <number of dice> <number of faces>'] = 'Simulates rolling an amount of dice with number of faces.'
    commands['!hello'] = "Bot responds with a salutation."

    msg = discord.Embed(title='Butter Bot',
                        description="Written by Squiekee with the discord.py wrapper.",
                        color=0xc5c3c0)
    for command, description in commands.items():
        msg.add_field(name=command, value=description, inline=False)
    #msg.add_field(name='Join Ur Discord/For Questions/Chilling', value='https://discord.gg/1a2b3c4d', inline=False)
    await ctx.send(embed=msg)


# Errors
@whoami.error
async def whoami(ctx, error):
    if isinstance(error, MissingPermissions):
        text = f'Sorry {ctx.message.author}, you do not have permissions to do that!'
        await ctx.send(text)

@roll.error
async def roll(ctx, error):
    text = ''
    if isinstance(error, CommandInvokeError):
        text = f'Yo, chill on the dice {ctx.message.author.name}! Lower the quantity and faces.'
        #Send to logging channel        await logChan().send(text)
    elif isinstance(error, BadArgument):
        text = f'You okay, {ctx.message.author.name}? Try using numbers next time.'
    await ctx.send(text)


# Run
bot.run(TOKEN)