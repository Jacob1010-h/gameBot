import asyncio
import os

from datetime import datetime
import discord
import numpy as np
from dotenv import load_dotenv
from prettytable import PrettyTable
from scipy.signal import convolve2d
from discord.ext import commands

p = PrettyTable()

board_np = np.zeros((6, 7))

SIZE = board_np.shape
SIZE_ROW = SIZE[0]
SIZE_COL = SIZE[1]

USER_INPUT = "Please input the colum Player %i\n"

NOT_VALID_INPUT = "Please enter a valid input Player %i\n"

INVALID_MOVE = "Invalid move please try again Player %i\n"

allowed = ["1", "2", "3", "4", "5", "6", "7"]

# possible wins
horizontal_kernel = np.array([[1, 1, 1, 1]])
vertical_kernel = np.transpose(horizontal_kernel)
diag1_kernel = np.eye(4, dtype=np.uint8)
diag2_kernel = np.fliplr(diag1_kernel)
detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]


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


class Users:
    player1 = None
    player2 = None

    def __init__(self):
        self.player1 = None
        self.player2 = None


class Player:
    player = 1
    current_player = ""
    temp_last = ""
    p1moves = []
    p2moves = []

    def __init__(self):
        self.player = 1
        self.current_player = ""
        self.temp_last = ""
        self.p1moves = []
        self.p2moves = []


async def winning_move(board):
    for kernel in detection_kernels:
        if (convolve2d(board == Player.player, kernel, mode="valid") == 4).any():
            return True
    return False


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


async def is_valid_move(x, y):
    if 0 < y <= SIZE_COL:
        if board_np[x, y - 1] == 0:
            return True
    return False


async def use_input(ctx, input_col):
    input_col = int(input_col)
    if await is_valid_move(0, input_col):
        board_np[0, input_col - 1] = Player.player
        return True
    else:
        await ctx.send(INVALID_MOVE % Player.player)
        return False


async def print_board_to_c(ctx):
    result1 = np.where(board_np == 0, " ", board_np)
    result2 = np.where(board_np == 1, "1", result1)
    result = np.where(board_np == 2, "2", result2)
    sep = '+===+===+===+===+===+===+===+'
    field = '| 1 | 2 | 3 | 4 | 5 | 6 | 7 |'
    for row in result:
        p.add_row(row)
    p.header = False
    p.border = True
    p.padding_width = 1
    p.horizontal_char = "="
    p.float_format = '.0'
    movesp1 = str("\n".join(Player.p1moves))
    movesp2 = str("\n".join(Player.p2moves))
    print_to_c(sep + "\n" + field + "\n" + p.get_string())
    p.clear()


async def print_board(ctx):
    result1 = np.where(board_np == 0, " ", board_np)
    result2 = np.where(board_np == 1, "1", result1)
    result = np.where(board_np == 2, "2", result2)
    sep = '+===+===+===+===+===+===+===+'
    field = '| 1 | 2 | 3 | 4 | 5 | 6 | 7 |'
    for row in result:
        p.add_row(row)
    p.header = False
    p.border = True
    p.padding_width = 1
    p.horizontal_char = "="
    p.float_format = '.0'
    movesp1 = str("\n".join(Player.p1moves))
    movesp2 = str("\n".join(Player.p2moves))
    # print(movesp1)
    # print(movesp2)
    em = discord.Embed(title=f"Player {Player.player}",
                       description='```' + sep + "\n" + field + "\n" + p.get_string() + '```',
                       color=ctx.author.color)
    if len(Player.p1moves) != 0:
        em.add_field(name="Player 1",
                     value=movesp1)
    if len(Player.p2moves) != 0:
        em.add_field(name="Player 2",
                     value=movesp2)
    await ctx.send(embed=em)
    p.clear()


async def fall_edit(pp, xi, yi):
    for i in range(SIZE_ROW - 1):  # loop through board
        if xi != SIZE_ROW - 1:  # if number is at the bottom row
            # move cell down if there is available space
            if board_np[xi + 1][yi] == 0:
                board_np[xi][yi] = 0
                xi += 1
                board_np[xi][yi] = pp


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
    async def start_game(self, ctx, player2=None):
        global board_np
        Users.player1 = ctx.author
        Users.player2 = player2
        # print(Users.player2)
        await ctx.message.delete()
        await ctx.send("Checking player's two status...")
        if Users.player2 is None:
            await ctx.send("No player 2 given.")
        if Users.player2 is not None:
            Users.player2 = str(await self.bot.fetch_user(Users.player2[2:-1]))
            # print(Users.player2)
            players = []
            for guild in self.bot.guilds:
                for member in guild.members:
                    players.append(str(member))

            if Users.player2 not in players:
                await ctx.send(f"Cannot find {Users.player2}")

            if Users.player2 in players:
                await ctx.send(f"{ctx.author} is starting a game with {Users.player2}")
                print_to_c(f"{ctx.author} is starting a game with {Users.player2}")
                board_np = np.zeros((6, 7))
                await print_board(ctx)

    @commands.command()
    async def move(self, ctx, col=None):
        global board_np
        Player.current_player = ctx.author
        # print(Player.current_player, type(Player.current_player))
        # print(Player.temp_last, type(Player.temp_last))
        # print(f"ctx: {ctx.author}", type(ctx.author))
        # print(f"p2: {Users.player2}", type(Users.player2))
        # print(f"p1: {Users.player1}", type(Users.player1))
        if Users.player2 is not None and Users.player1 is not None:
            if str(ctx.author) == str(Users.player1) or str(ctx.author) == str(Users.player2):
                if str(Player.temp_last) != str(Player.current_player):
                    await ctx.message.delete()
                    if await use_input(ctx, col):
                        if Player.player == 1:
                            Player.p1moves.append(col)
                        elif Player.player == 2:
                            Player.p2moves.append(col)
                        await fall(ctx)
                        if await winning_move(board_np):
                            await ctx.send(f"Player {Player.player} has won!")
                            Player.p1moves = []
                            Player.p2moves = []
                            if Player.player == 1:
                                print_to_c(f"{Users.player1} has won a game against {Users.player2}!\n")
                                await print_board_to_c(ctx)
                            elif Player.player == 2:
                                print_to_c(f"{Users.player2} has won a game against {Users.player1}!\n")
                                await print_board_to_c(ctx)
                            board_np = np.zeros((6, 7))
                        if Player.player == 1:
                            Player.player = 2
                        elif Player.player == 2:
                            Player.player = 1
                        Player.temp_last = Player.current_player


def setup(bot):
    bot.add_cog(ConnectFour(bot))
