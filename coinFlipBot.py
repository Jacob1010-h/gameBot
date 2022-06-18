# coinBot.py
import asyncio
import os
import random
from datetime import datetime

from discord.ext import commands
from dotenv import load_dotenv

def printToConsole(input):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(LINE)
    print(dt_string)
    print(input)
    print(LINE)
    print("\n")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
HELP = os.getenv('DISCORD_COIN_HELP')
LINE = os.getenv('CONSOLE_LINE')
    
@commands.command()
async def flipHelp(ctx):
    help = HELP
    author = ctx.author
    input = f'{author} required assistance with coin bot.'
    printToConsole(input)
    await ctx.send(help)
    
@commands.command(name='flip', pass_context=True)
async def flip(ctx, number=None):
    heads_tails = ['Heads', 'Tails']
    author = ctx.author
    
    if number != None:
        await flip_many(ctx, author, number, heads_tails)
    else:
        response = random.choice(heads_tails)
        input= f'{author} flipped a coin!' + "\n     " + "1. " + response
        printToConsole(input)
        await ctx.send(response)    
    
@commands.command()
async def flip_many(ctx, author, number, choice):
    num = int(number)
    input = f'{author} flipped many coins!'
    coinFlipsInput = []
    coinFlipsInput.append(input)
    coinFlips = []
    for i in range(num):
        response = random.choice(choice)
        coinInput = "     " + f"{i+1}. " + response
        coinFlipsInput.append(coinInput)
        coinFlips.append(response)
    for flipResult in coinFlips:
        await asyncio.sleep(0.025)
        await ctx.send(flipResult)        
    printToConsole('\n'.join(coinFlipsInput))
    
def setup(bot):
    bot.add_command(flipHelp)
    bot.add_command(flip_many)
    bot.add_command(flip)
    