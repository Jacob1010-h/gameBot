from discord.ext import commands


class Modes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coin_flip(self, ctx):
        self.bot.load_extension("cogs.coinFlipBot")
        await ctx.send("```Coin Flip Bot is online!```")

    @commands.command()
    async def connect_4(self, ctx):
        self.bot.load_extension("cogs.connectFour")
        await ctx.send("```Connect Four Bot is online!```")


def setup(bot):
    bot.add_cog(Modes(bot))
