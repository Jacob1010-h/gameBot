# Importing the modules that are needed for the cog to work.
import asyncio
import os
from datetime import datetime
import random
# from bot import print_to_c
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
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


async def flip_many(ctx, author, number, choice):
    """
    It takes a user's input, and then flips a coin that many times.
    
    :param ctx: The context of the command
    :param author: The author of the message
    :param number: The number of coins to flip
    :param choice: This is the list of choices that the bot will choose from
    """
    num = int(number)
    inp = f'{author} flipped many coins!'
    coin_flips_input = [inp]
    coin_flips = []
    for i in range(num):
        response = random.choice(choice)
        coin_input = "     " + f"{i + 1}. " + response
        coin_flips_input.append(coin_input)
        if response == 'Heads':
            coin_flips.append(coin_input + ":full_moon:")
        else:
            coin_flips.append(coin_input + ":last_quarter_moon:")

    pfp = ctx.author.avatar_url
    em = discord.Embed(title="**Coin Flips**",
                       color=ctx.author.color)
    em.add_field(name=f"{number} Flips",
                 value='\n'.join(coin_flips))
    em.set_author(name=f"{ctx.author}",
                  icon_url=pfp)

    await ctx.message.delete()
    await ctx.send(embed=em)
    print_to_c('\n'.join(coin_flips_input))


class CoinFlip(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='flip', pass_context=True)
        """
        It takes a number and a list of strings, and returns a list of strings with the same length as the
        number
        
        :param ctx: The context of the command
        :param number: The number of times you want to flip the coin
        """
    async def flip(self, ctx, number=None):
        heads_tails = ['Heads', 'Tails']
        author = ctx.author

        if number is not None:
            await flip_many(ctx, author, number, heads_tails)
        else:
            response = random.choice(heads_tails)
            pfp = ctx.author.avatar_url
            inp = f'{author} flipped a coin!' + "\n     " + "1. " + response
            print_to_c(inp)
            em = discord.Embed(title=f"**{response}**",
                               color=ctx.author.color)
            em.set_author(name=f"{ctx.author}",
                          icon_url= pfp)

            await ctx.message.delete()
            await ctx.send(embed=em)


def setup(bot):
    """
    It adds the cog to the bot
    
    :param bot: The bot object
    """
    bot.add_cog(CoinFlip(bot))
