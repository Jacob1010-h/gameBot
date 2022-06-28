# Importing the os module, the datetime module, the discord.ext module, the dotenv module, and loading
# the dotenv module. It is also setting the LINE variable to the CONSOLE_LINE environment variable.
import os
from datetime import datetime

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


class Owner(commands.Cog):

    def __init__(self, bot):
        """
        It initializes the cog
        
        :param bot: The bot object
        """
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        """
        It deletes the message that triggered the command, sends a message saying "Shutting down...",
        prints "Shutting down..." to the console, and then exits the program
        
        :param ctx: The context of the message
        """
        await ctx.message.delete()
        await ctx.send("Shutting down...")
        print_to_c("Shutting down...")
        exit()

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def clear(self, ctx, amount=5):
        """
        It deletes the command message and then deletes the amount of messages specified by the user
        
        :param ctx: The context of where the command was used
        :param amount: The amount of messages to delete, defaults to 5 (optional)
        """
        if amount == -00:
            await ctx.channel.purge()
        else:
            await ctx.message.delete()
            await ctx.channel.purge(limit=amount)


def setup(bot):
    """
    It adds the cog to the bot
    
    :param bot: The bot object
    """
    bot.add_cog(Owner(bot))
