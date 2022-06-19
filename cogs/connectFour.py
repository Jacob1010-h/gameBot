import numpy as np
from prettytable import PrettyTable
from scipy.signal import convolve2d
from discord.ext import commands

p = PrettyTable()

board_np = np.random.randint(3, size=(6, 7))

SIZE = board_np.shape
SIZE_ROW = SIZE[0]
SIZE_COL = SIZE[1]

USER_INPUT = "Please input the colum Player %i\n"

NOT_VALID_INPUT = "Please enter a valid input Player %i\n"

INVALID_MOVE = "Invalid move please try again Player %i\n"

allowed = set("1234567")


async def create_num_arr():
    # list 1
    l1 = np.where(board_np == 1)
    l1 = list(zip(l1[0], l1[1]))
    result1 = l1[::-1]
    # list 2
    l2 = np.where(board_np == 2)
    l2 = list(zip(l2[0], l2[1]))
    result2 = l2[::-1]
    return result1, result2


async def print_board(ctx):
    for row in board_np:
        p.add_row(row)
    p.header = False
    p.border = True
    p.padding_width = 1
    p.horizontal_char = "="
    p.float_format = "0.0"
    await ctx.send('```' +
                   p.get_string() +
                   '```'
                   )
    p.clear()


async def fall_edit(player, xi, yi):
    for i in range(SIZE_ROW - 1):  # loop through board
        if xi != SIZE_ROW - 1:  # if number is at the bottom row
            # move cell down if there is available space
            if board_np[xi + 1][yi] == 0:
                board_np[xi][yi] = 0
                xi += 1
                board_np[xi][yi] = player


async def fall(ctx):
    for i in range(0, 2):
        result1, result2 = await create_num_arr()
        # separate x and y
        for xi, yi in result1:
            # edit board
            await fall_edit(1, xi, yi)

        # separate x and y
        for xi, yi in result2:
            # edit board
            await fall_edit(2, xi, yi)
    await print_board(ctx)


class ConnectFour(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test_board(self, ctx):
        await print_board(ctx)
        await fall(ctx)


def setup(bot):
    bot.add_cog(ConnectFour(bot))
