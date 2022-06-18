import os
import time
import numpy as np

from termcolor import colored

board_np = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ])

board = [
    ['0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0']
]

BOARD_LENGTH_ROW = 6
BOARD_LENGTH_COL = 7

SEPARATOR = '+===+===+===+===+===+===+===+'


def getCell(x, y):
    return board[x][y]


def setCell(x, y, value):
    board[x][y] = str(value)


def printBoard():
    for row in range(len(board)):
        if row == 0:
            print(SEPARATOR)
        for col in range(len(board[row])):
            if col == 0:
                print('| ', end='')
            if getCell(row, col) == '1':
                print(colored(getCell(row, col), 'green'), end=' | ')
            elif getCell(row, col) == '2':
                print(colored(getCell(row, col), 'cyan'), end=' | ')
            else:
                print(colored(getCell(row, col), 'red'), end=' | ')
        print("")
        print(SEPARATOR)


def clear():
    os.system('cls')


def fall():
    for row in reversed(range(len(board) - 1)):
        for col in reversed(range(len(board[row]))):
            if getCell(row, col) == '1' or getCell(row, col) == '2':
                for i in range(row, (len(board) - 1)):
                    if getCell(i, col) == '1' and getCell(i+1, col) == '0':
                        setCell(i, col, 0)
                        setCell(i + 1, col, 1)
                    elif getCell(i, col) == '2' and getCell(i+1, col) == '0':
                        setCell(i, col, 0)
                        setCell(i + 1, col, 2)
    os.system('cls')
    printBoard()
    time.sleep(1)


def has_won():
    count_1 = 0
    count_2 = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            # print(f"{row} and {col}; cellValue: {getCell(row, col)}")
            if getCell(row, col) == '1':
                count_1 += 1
                if getCell(row, col) == '0' or getCell(row, col) == '1':
                    count_2 = 0
            elif getCell(row, col) == '2':
                if getCell(row, col) == '0' or getCell(row, col) == '2':
                    count_1 = 0
                count_2 += 1
            # print(f"row and col: {row} and {col}; cellValue: {getCell(row, col)}; count_1: {count_1}")
            # print(f"row and col: {row} and {col}; cellValue: {getCell(row, col)}; count_2: {count_2}")
            if count_1 == 4 or count_2 == 4:
                return True
        count_1 = 0
        count_2 = 0


def is_legal_move(row, col):
    if 0 < col+1 < BOARD_LENGTH_COL+1 and getCell(row, col) == '0':
        return True
    else:
        return False


def run():
    printBoard()
    player = 1
    row = 0
    running = 1
    legal = 0
    while running == 1:
        if player == 1:
            print(f"Please input your column Player {player}:\n")
            while legal == 0:
                col = input()
                col = int(col)
                if is_legal_move(row, col-1):
                    setCell(row, col-1, player)
                    player = 2
                    legal = 1
                else:
                    print(f"Invalid move Player {player}, try again.\n")

        else:
            print(f"Please input your column Player {player}:\n")
            while legal == 0:
                col = input()
                col = int(col)
                if is_legal_move(row, col-1):
                    setCell(row, col - 1, player)
                    player = 1
                    legal = 1
                else:
                    print(f"Invalid move Player {player}, try again.\n")
        fall()
        legal = 0
        if has_won():
            if player == 2:
                print(f"Player {player-1} has won the game!")
            elif player == 1:
                print(f"Player {player + 1} has won the game!")
            break


if __name__ == '__main__':
    run()
