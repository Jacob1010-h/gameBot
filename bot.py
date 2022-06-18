# bot.py
import asyncio
from datetime import datetime
from distutils import extension
from imp import load_compiled
import os
from discord.ext.commands import CommandNotFound

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
HELP = os.getenv('DISCORD_HELP')
WRONG_MODE = os.getenv('DISCORD_WRONG_MODE')
LINE = os.getenv('CONSOLE_LINE')


def printToConsole(input):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(LINE)
    print(dt_string)
    print(input)
    print(LINE)
    print("\n")


bot = commands.Bot(command_prefix='!', case_insensitive=True, help_command=None)
bot.coin_bot = 0


@bot.event
async def on_ready():
    input = f'{bot.user.name} has connected to Discord!'
    printToConsole(input)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send(WRONG_MODE)
    else:
        raise error


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Shutting down...")
    printToConsole("Shutting down...")
    exit()


@bot.command()
async def help(ctx):
    help = HELP
    author = ctx.author
    input = f'{author} required assistance with game bot.'
    printToConsole(input)
    await ctx.send(help)


@bot.command()
async def flipMode(ctx):
    if bot.coin_bot == 0:
        await ctx.send("Transfering user to Coin Bot...")
        bot.load_extension("coinFlipBot")
        if bot.extensions != None:
            await ctx.channel.purge(limit=2)
            await ctx.send("```Coin Bot activated```")
            author = ctx.author
            printToConsole(f"Coin Bot has been activated by {author}!")
            bot.coin_bot = 1
    else:
        await ctx.send("```Coin Bot is currently running```")


bot.run(TOKEN)
