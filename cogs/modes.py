from discord.ext import commands


class Modes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coin_flip(self, ctx):
        self.bot.load_extension("cogs.sub-cogs.coinFlip")
        await ctx.message.delete()
        await ctx.send("```Coin Flip Bot is online!```")

    @commands.command()
    async def connect_4(self, ctx):
        self.bot.load_extension("cogs.sub-cogs.connectFour")
        await ctx.message.delete()
        await ctx.send("```Connect Four Bot is online!```")


def setup(bot):
    bot.add_cog(Modes(bot))
