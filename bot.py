# bot.py
# Importing the libraries that are needed for the bot to run.
from datetime import datetime
import os

import discord
from discord.ext.commands import CommandNotFound

from discord.ext import commands
from dotenv import load_dotenv

# Allowing the bot to see the members of the server.
intents = discord.Intents.default()
intents.members = True

# Loading the .env file and getting the token and the line to print to the console.
load_dotenv()
TOKEN = os.getenv('/token.env/DISCORD_TOKEN')
LINE = os.getenv('CONSOLE_LINE')


def print_to_c(imp):
    """
    It prints a line, the current date and time, the input, another line, and a new line
    
    :param imp: The string to be printed
    """
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(LINE)
    print(dt_string)
    print(imp)
    print(LINE)
    print("\n")


# Creating a bot object and removing the default help command.
bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    """
    It prints a message to the console when the bot is ready
    """
    imp = f'{bot.user.name} has connected to Discord!'
    print_to_c(imp)
    bot.load_extension("cogs.owner")
    bot.load_extension("cogs.modes")


@bot.event
async def on_command_error(ctx, error):
    """
    If the command is not found, send a message to the user saying that the command is not available.
    
    :param ctx: The context of where the command was used
    :param error: The error that was raised
    """
    if isinstance(error, CommandNotFound):
        await ctx.send('This command is not available, please type !help for a list of all possible commands.')


@bot.group(name='help', invoke_without_command=True)
async def _help(ctx):
    """
    It sends an embed with a list of commands.
    
    :param ctx: The context of where the command was used
    """
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
    """
    It sends an embed with the syntax of the clear command.
    
    :param ctx: The context of where the command was used
    """
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
    """
    It sends an embed with the syntax of the shutdown command.
    
    :param ctx: The context of where the command was used
    """
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
    """
    It sends an embed with the syntax of the command.
    
    :param ctx: The context of where the command was used. For example, if you used the command in a
    guild channel, ctx.guild will be the guild the command was used in
    """
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
    """
    It sends an embed with a description, syntax, and a field.
    
    :param ctx: The context of where the command was used
    """
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
    """
    It sends an embed with a description of the command
    
    :param ctx: The context of where the command was used
    """
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
    """
    It sends an embed with a description of how to start a game of connect 4
    
    :param ctx: The context of where the command was used
    """
    em = discord.Embed(title="Start Game",
                       description="Starts a new game of connect four, overwriting any game that was previously being "
                                   "played.",
                       color=ctx.author.color)
    em.add_field(name="**Syntax**",
                 value="!start_game @<user>")

    await ctx.message.delete()
    await ctx.send(embed=em)
    print_to_c(f'{ctx.author} needed help with the starting a connect 4 game.')


@_help.command()
async def move(ctx):
    """
    It deletes the message that the user sent, and then sends an embed with the syntax for the command.
    
    :param ctx: The context of the command
    """
    em = discord.Embed(title="Move",
                       description="Makes a move on the active connect four board.",
                       color=ctx.author.color)
    em.add_field(name="**Syntax**",
                 value="!move <column>")

    await ctx.message.delete()
    await ctx.send(embed=em)
    print_to_c(f'{ctx.author} needed help with moving a piece in a connect four game.')


# Running the bot.
bot.run(TOKEN)
