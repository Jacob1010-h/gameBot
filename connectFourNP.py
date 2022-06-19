import numpy as np
from prettytable import PrettyTable
from scipy.signal import convolve2d

board_np = np.zeros((6, 7))
# board_np = np.random.randint(3, size=(6, 7))
# # board_np = np.eye(6, 7)

SEPARATOR = "\n-------------------------\n"

p = PrettyTable()

SIZE = board_np.shape
SIZE_ROW = SIZE[0]
SIZE_COL = SIZE[1]

USER_INPUT = "Please input the colum Player %i\n"

NOT_VALID_INPUT = "Please enter a valid input Player %i\n"

INVALID_MOVE = "Invalid move please try again Player %i\n"

allowed = set("1234567")

# possible wins
horizontal_kernel = np.array([[1, 1, 1, 1]])
vertical_kernel = np.transpose(horizontal_kernel)
diag1_kernel = np.eye(4, dtype=np.uint8)
diag2_kernel = np.fliplr(diag1_kernel)
detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]


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


def is_valid_move(x, y):
    if 0 < y <= SIZE_COL:
        if board_np[x, y - 1] == 0:
            return True
    return False


def use_input(input_col, player):
    input_col = int(input_col)
    if is_valid_move(0, input_col):
        board_np[0, input_col - 1] = player
    else:
        print(INVALID_MOVE % player)
        return False


def winning_move(board, player):
    for kernel in detection_kernels:
        if (convolve2d(board == player, kernel, mode="valid") == 4).any():
            return True
    return False


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
    player = 1
    print_board()
    while True:
        print(USER_INPUT % player)
        var = input()
        if var and allowed.issuperset(var):
            if player == 1:
                use_input(var, 1)
                fall()
                if winning_move(board_np, player):
                    print(f"Player {player} has won!")
                    break
                player = 2
            else:
                use_input(var, 2)
                fall()
                if winning_move(board_np, player):
                    print(f"Player {player} has won!")
                    break
                player = 1
        else:
            print(NOT_VALID_INPUT % player)


if __name__ == '__main__':
    run()
