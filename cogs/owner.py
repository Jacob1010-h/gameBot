import os
from datetime import datetime

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


class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.message.delete()
        await ctx.send("Shutting down...")
        print_to_c("Shutting down...")
        exit()

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def clear(self, ctx, amount=5):
        if amount == -00:
            await ctx.channel.purge()
        else:
            await ctx.message.delete()
            await ctx.channel.purge(limit=amount)


def setup(bot):
    bot.add_cog(Owner(bot))
