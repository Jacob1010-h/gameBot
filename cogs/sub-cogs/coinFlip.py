import asyncio
import os
from datetime import datetime
import random
# from bot import print_to_c
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
LINE = os.getenv('CONSOLE_LINE')


def print_to_c(imp):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(LINE)
    print(dt_string)
    print(imp)
    print(LINE)
    print("\n")


async def flip_many(ctx, author, number, choice):
    num = int(number)
    inp = f'{author} flipped many coins!'
    coin_flips_input = [inp]
    coin_flips = []
    for i in range(num):
        response = random.choice(choice)
        coin_input = "     " + f"{i + 1}. " + response
        coin_flips_input.append(coin_input)
        coin_flips.append(response)
    for flipResult in coin_flips:
        await asyncio.sleep(0.025)
        await ctx.send(flipResult)
    print_to_c('\n'.join(coin_flips_input))


class CoinFlip(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='flip', pass_context=True)
    async def flip(self, ctx, number=None):
        heads_tails = ['Heads', 'Tails']
        author = ctx.author

        if number is not None:
            await flip_many(ctx, author, number, heads_tails)
        else:
            response = random.choice(heads_tails)
            inp = f'{author} flipped a coin!' + "\n     " + "1. " + response
            print_to_c(inp)
            await ctx.send(response)


def setup(bot):
    bot.add_cog(CoinFlip(bot))
