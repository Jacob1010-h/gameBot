# bot.py
import asyncio
from datetime import datetime
from distutils import extension
from imp import load_compiled
import os

import discord
from discord.ext.commands import CommandNotFound

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
HELP = os.getenv('DISCORD_HELP')
WRONG_MODE = os.getenv('DISCORD_WRONG_MODE')
LINE = os.getenv('CONSOLE_LINE')
COIN_ACTIVATION = os.getenv('COIN_BOT_ACTIVATION_HELP')
ID = os.getenv('OWNER_ID')


def print_to_c(imp):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(LINE)
    print(dt_string)
    print(imp)
    print(LINE)
    print("\n")


bot = commands.Bot(command_prefix='!', case_insensitive=True)
bot.remove_command("help")


# bot.coin_bot = 0


@bot.event
async def on_ready():
    imp = f'{bot.user.name} has connected to Discord!'
    print_to_c(imp)
    bot.load_extension("cogs.owner")
    bot.load_extension("cogs.modes")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send(WRONG_MODE)


@bot.group(name='help', invoke_without_command=True)
async def _help(ctx):
    em = discord.Embed(title="Help",
                       description="Use !help <command> for extended information on a command.",
                       color=ctx.author.color)
    if await bot.is_owner(ctx.author):
        em.add_field(name="Moderation",
                     value="clear\nshutdown")
    em.add_field(name="Games",
                 value="coin_flip\nconnect_four")

    await ctx.send(embed=em)


@_help.command()
async def clear(ctx):
    em = discord.Embed(title="Clear",
                       description="Clears the an amount of messages sent, in no input is given, "
                                   "it will clear 5",
                       color=ctx.author.color)
    em.add_field(name="**Syntax**",
                 value="!clear <number>")

    await ctx.send(embed=em)


@_help.command()
async def shutdown(ctx):
    em = discord.Embed(title="Shutdown",
                       description="Completely shuts the bot down.",
                       color=ctx.author.color)
    em.add_field(name="**Syntax**",
                 value="!shutdown")

    await ctx.send(embed=em)


@_help.command()
async def coin_flip(ctx):
    em = discord.Embed(title="Coin Flip Bot Activation",
                       description="Activates the Coin Flip Bot, allowing you to flip a coin",
                       color=ctx.author.color)
    em.add_field(name="**Syntax**",
                 value="!coin_flip")

    await ctx.send(embed=em)


@_help.command()
async def connect_four(ctx):
    em = discord.Embed(title="Connect Four Bot Activation",
                       description="Activates the Connect Four Bot, allowing you to play a game of connect four",
                       color=ctx.author.color)
    em.add_field(name="**Syntax**",
                 value="!connect_four")

    await ctx.send(embed=em)


bot.run(TOKEN)
