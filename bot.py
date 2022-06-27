# bot.py
from datetime import datetime
import os

import discord
from discord.ext.commands import CommandNotFound

from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
LINE = os.getenv('CONSOLE_LINE')


def print_to_c(imp):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(LINE)
    print(dt_string)
    print(imp)
    print(LINE)
    print("\n")


bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    imp = f'{bot.user.name} has connected to Discord!'
    print_to_c(imp)
    bot.load_extension("cogs.owner")
    bot.load_extension("cogs.modes")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send('This command is not available, please type !help for a list of all possible commands.')


@bot.group(name='help', invoke_without_command=True)
async def _help(ctx):
    em = discord.Embed(title="Help",
                       description="Use !help <command> for extended information on a command.",
                       color=ctx.author.color)
    if await bot.is_owner(ctx.author):
        em.add_field(name="Moderation",
                     value="clear\nshutdown")
    em.add_field(name="Games : Activations",
                 value="coin_flip\nconnect_4")
    em.add_field(name="Games : Commands",
                 value="flip\nstart_game, move")

    await ctx.message.delete()
    await ctx.send(embed=em)
    print_to_c(f'{ctx.author} needed help with the bot.')


@_help.command()
async def clear(ctx):
    em = discord.Embed(title="Clear",
                       description="Clears the an amount of messages sent, in no input is given, "
                                   "it will clear 5",
                       color=ctx.author.color)
    em.add_field(name="**Syntax**",
                 value="!clear <number>")

    await ctx.message.delete()
    await ctx.send(embed=em)
    print_to_c(f'{ctx.author} needed help with the clear command.')


@_help.command()
async def shutdown(ctx):
    em = discord.Embed(title="Shutdown",
                       description="Completely shuts the bot down.",
                       color=ctx.author.color)
    em.add_field(name="**Syntax**",
                 value="!shutdown")

    await ctx.message.delete()
    await ctx.send(embed=em)
    print_to_c(f'{ctx.author} needed help with the shutdown command.')


@_help.command()
async def coin_flip(ctx):
    em = discord.Embed(title="Bot Activation : Coin Flip ",
                       description="Activates the Coin Flip Bot, allowing you to flip a coin",
                       color=ctx.author.color)
    em.add_field(name="**Syntax**",
                 value="!coin_flip")

    await ctx.message.delete()
    await ctx.send(embed=em)
    print_to_c(f'{ctx.author} needed help with the coin_flip bot activation')


@_help.command()
async def flip(ctx):
    em = discord.Embed(title="Flip",
                       description="Flips a coin, giving a result of heads or tails. If a number is specified then it "
                                   "will flip so many times. To use this command you must activate the coin flip bot.",
                       color=ctx.author.color)
    em.add_field(name="**Syntax**",
                 value="!flip <number>")

    await ctx.message.delete()
    await ctx.send(embed=em)
    print_to_c(f'{ctx.author} needed help with flipping a coin.')


@_help.command()
async def connect_4(ctx):
    em = discord.Embed(title="Bot Activation : Connect Four",
                       description="Activates the Connect Four Bot, allowing you to play a game of connect four.",
                       color=ctx.author.color)
    em.add_field(name="**Syntax**",
                 value="!connect_4")

    await ctx.message.delete()
    await ctx.send(embed=em)
    print_to_c(f'{ctx.author} needed help with the connect_four bot activation.')


@_help.command()
async def start_game(ctx):
    em = discord.Embed(title="Start Game",
                       description="Starts a new game of connect four, overwiting any game that was previously being "
                                   "played.",
                       color=ctx.author.color)
    em.add_field(name="**Syntax**",
                 value="!start_game @<user>")

    await ctx.message.delete()
    await ctx.send(embed=em)
    print_to_c(f'{ctx.author} needed help with the starting a connect 4 game.')


@_help.command()
async def move(ctx):
    em = discord.Embed(title="Move",
                       description="Makes a move on the active connect four board.",
                       color=ctx.author.color)
    em.add_field(name="**Syntax**",
                 value="!move <column>")

    await ctx.message.delete()
    await ctx.send(embed=em)
    print_to_c(f'{ctx.author} needed help with moving a piece in a connect four game.')


bot.run(TOKEN)
