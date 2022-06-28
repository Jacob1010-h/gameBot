# It's importing all the modules that are needed for the bot to work.
import asyncio
import os

from datetime import datetime
import discord
import numpy as np
from dotenv import load_dotenv
from prettytable import PrettyTable
from scipy.signal import convolve2d
from discord.ext import commands

# It's creating a table that will be used to print the board.
p = PrettyTable()

# It's creating a 6x7 matrix of zeros.
board_np = np.zeros((6, 7))

# It's getting the size of the board and setting the SIZE_ROW and SIZE_COL variables to the size of
# the board.
SIZE = board_np.shape
SIZE_ROW = SIZE[0]
SIZE_COL = SIZE[1]

# It's creating a string that will be used to print the message to the user.
USER_INPUT = "Please input the colum Player %i\n"

NOT_VALID_INPUT = "Please enter a valid input Player %i\n"

INVALID_MOVE = "Invalid move please try again Player %i\n"

# It's creating a list of possible moves.
allowed = ["1", "2", "3", "4", "5", "6", "7"]

# It's creating a list of possible wins.
horizontal_kernel = np.array([[1, 1, 1, 1]])
vertical_kernel = np.transpose(horizontal_kernel)
diag1_kernel = np.eye(4, dtype=np.uint8)
diag2_kernel = np.fliplr(diag1_kernel)
detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]


# It's loading the .env file and getting the token and the console line.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
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


# The Users class is a class that has two attributes, player1 and player2, which are both set to None
class Users:
    player1 = None
    player2 = None

    def __init__(self):
        self.player1 = None
        self.player2 = None


# The Player class is used to keep track of the current player, the last player, and the moves of each
# player.
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
    """
    It checks if there are any 4-in-a-rows in the board
    
    :param board: The board to check for a winning move
    :return: a boolean value.
    """
    for kernel in detection_kernels:
        if (convolve2d(board == Player.player, kernel, mode="valid") == 4).any():
            return True
    return False


async def create_num_arr():
    """
    It takes a 2D array and returns two lists of tuples, where each tuple is a coordinate of a 1 or 2 in
    the array, flipping the board.
    :return: A tuple of two lists.
    """
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
    """
    If the column is valid and the space is empty, return True, otherwise return False
    
    :param x: the row number of the board
    :param y: the column number
    :return: The function is_valid_move() is returning a boolean value.
    """
    if 0 < y <= SIZE_COL:
        if board_np[x, y - 1] == 0:
            return True
    return False


async def use_input(ctx, input_col):
    """
    If the move is valid, then the player's move is added to the board
    
    :param ctx: The context of the message
    :param input_col: The column the player wants to drop their piece in
    :return: a boolean value.
    """
    input_col = int(input_col)
    if await is_valid_move(0, input_col):
        board_np[0, input_col - 1] = Player.player
        return True
    else:
        await ctx.send(INVALID_MOVE % Player.player)
        return False


async def print_board_to_c(ctx):
    """
    It takes the board_np array, replaces the 0's with spaces, the 1's with 1's, and the 2's with 2's.
    Then it prints the board to the console.
    
    :param ctx: The context of the message
    """
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
    """
    It prints the board in a nice way.
    
    :param ctx: The context of the command
    """
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
    """
    If the cell is not at the bottom row, and the cell below it is empty, then move the cell down one
    row.
    
    :param pp: the number that is being moved
    :param xi: x index of the cell
    :param yi: column
    """
    for i in range(SIZE_ROW - 1):  # loop through board
        if xi != SIZE_ROW - 1:  # if number is at the bottom row
            # move cell down if there is available space
            if board_np[xi + 1][yi] == 0:
                board_np[xi][yi] = 0
                xi += 1
                board_np[xi][yi] = pp


async def fall(ctx):
    """
    It creates a 2D array of numbers, then it separates the x and y coordinates, then it edits the board
    with the x and y coordinates, then it prints the board.
    
    :param ctx: The context of the message
    """
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
        """
        It initializes the cog
        
        :param bot: The bot object
        """
        self.bot = bot

    @commands.command()
    async def start_game(self, ctx, player2=None):
        """
        It takes a user's ID and checks if that user is in the server. If they are, it starts a game.
        
        :param ctx: The context of the command
        :param player2: The player that the user wants to play with
        """
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
        """
        It's a command that allows players to play a game of connect 4.
        
        :param ctx: The context of the command
        :param col: The column the player wants to place their piece in
        """
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
    """
    It adds the cog to the bot
    
    :param bot: The bot object
    """
    bot.add_cog(ConnectFour(bot))
