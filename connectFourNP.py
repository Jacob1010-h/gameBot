import numpy as np
from prettytable import PrettyTable
from rich.console import Console

# board_np = np.zeros((6, 7))
board_np = np.random.randint(3, size=(6, 7))
# board_np = np.eye(6, 7)

SEPARATOR = "\n-------------------------\n"

p = PrettyTable()

console = Console()

SIZE = board_np.shape
SIZE_ROW = SIZE[0]
SIZE_COL = SIZE[1]

USER_INPUT = "Please input the colum Player %i"


def print_board():
    for row in board_np:
        p.add_row(row)
    p.header = False
    p.border = True
    p.padding_width = 1
    p.horizontal_char = "="
    p.float_format = "0.0"
    print(p)
    p.clear()


def create_num_arr():
    # list 1
    l1 = np.where(board_np == 1)
    l1 = list(zip(l1[0], l1[1]))
    result1 = l1[::-1]
    # list 2
    l2 = np.where(board_np == 2)
    l2 = list(zip(l2[0], l2[1]))
    result2 = l2[::-1]
    return result1, result2


def fall_edit(player, xi, yi):
    for i in range(SIZE_ROW - 1):  # loop through board
        if xi != SIZE_ROW - 1:  # if number is at the bottom row
            # move cell down if there is available space
            if board_np[xi + 1][yi] == 0:
                board_np[xi][yi] = 0
                xi += 1
                board_np[xi][yi] = player


def fall():
    for i in range(0, 2):
        result1, result2 = create_num_arr()
        # separate x and y
        for xi, yi in result1:
            # edit board
            fall_edit(1, xi, yi)

        # separate x and y
        for xi, yi in result2:
            # edit board
            fall_edit(2, xi, yi)
    print_board()


def run():
    print_board()
    fall()
    # print(USER_INPUT % 1)
    # input()


if __name__ == '__main__':
    run()
