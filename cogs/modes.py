import os
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv

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


class Modes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
        """
        It loads the coinFlip.py file and then sends a message to the channel saying that the bot is
        online.
        
        :param ctx: The context of where the command was used
        """
    async def coin_flip(self, ctx):
        self.bot.load_extension("cogs.sub-cogs.coinFlip")
        await ctx.message.delete()
        await ctx.send("```Coin Flip Bot is online!```")
        print_to_c("Coin Flip Bot is online!")

    @commands.command()
        """
        It loads the connectFour.py file and then sends a message to the channel saying that the bot is
        online.
        
        :param ctx: The context of where the command was used
        """
    async def connect_4(self, ctx):
        self.bot.load_extension("cogs.sub-cogs.connectFour")
        await ctx.message.delete()
        await ctx.send("```Connect Four Bot is online!```")
        print_to_c("Connect Four Bot is online!")


def setup(bot):
    bot.add_cog(Modes(bot))
