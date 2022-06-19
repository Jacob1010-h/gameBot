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
COIN_ACTIVATION = os.getenv('COIN_BOT_ACTIVATION_HELP')


def print_to_c(imp):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(LINE)
    print(dt_string)
    print(imp)
    print(LINE)
    print("\n")


bot = commands.Bot(command_prefix='!', case_insensitive=True)
# bot.coin_bot = 0


@bot.event
async def on_ready():
    imp = f'{bot.user.name} has connected to Discord!'
    print_to_c(imp)
    bot.load_extension("cogs.modes")


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
    print_to_c("Shutting down...")
    exit()


# @bot.command()
# async def connect_for_test(ctx):
#     bot.load_extension("connectFour")


@bot.command(pass_context=True)
@commands.is_owner()
async def clear(ctx, amount=5):
    if amount == -00:
        await ctx.channel.purge()
    else:
        await ctx.channel.purge(limit=amount)


# @bot.command()
# async def flip_mode(ctx):
#     """
#     Type !flip_mode to activate the coin bot and to run its commands.
#     """
#     if bot.coin_bot == 0:
#         await ctx.send("Transfering user to Coin Bot...")
#         bot.load_extension("coinFlipBot")
#         if bot.extensions is not None:
#             await ctx.channel.purge(limit=2)
#             await ctx.send("```Coin Bot activated```")
#             author = ctx.author
#             print_to_c(f"Coin Bot has been activated by {author}!")
#             bot.coin_bot = 1
#     else:
#         await ctx.send("```Coin Bot is currently running```")

bot.run(TOKEN)
