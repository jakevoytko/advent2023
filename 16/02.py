from collections import deque
from enum import Enum
import numpy as np
from itertools import chain

f = open('input.txt', 'r')

board = [[*line.strip()] for line in f]
f.close()

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

def travel(row, col, direction):
    if direction == Direction.UP:
        return row - 1, col, direction
    elif direction == Direction.RIGHT:
        return row, col + 1, direction
    elif direction == Direction.DOWN:
        return row + 1, col, direction
    elif direction == Direction.LEFT:
        return row, col - 1, direction

def bounce(row, col, direction, upRight):
    if upRight:
        if direction == Direction.UP:
            return row, col + 1, Direction.RIGHT
        elif direction == Direction.RIGHT:
            return row - 1, col, Direction.UP
        elif direction == Direction.DOWN:
            return row, col - 1, Direction.LEFT
        elif direction == Direction.LEFT:
            return row + 1, col, Direction.DOWN
    if direction == Direction.UP:
        return row, col - 1, Direction.LEFT
    elif direction == Direction.RIGHT:
        return row + 1, col, Direction.DOWN
    elif direction == Direction.DOWN:
        return row, col + 1, Direction.RIGHT
    elif direction == Direction.LEFT:
        return row - 1, col, Direction.UP

def youGotPiped(row, col, direction, vertical):
    if vertical:
        if direction == Direction.UP or direction == Direction.DOWN:
            return [travel(row, col, direction)]
        elif direction == Direction.RIGHT or direction == Direction.LEFT:
            return [(row-1, col, Direction.UP), (row+1, col, Direction.DOWN)]
    else:
        if direction == Direction.UP or direction == Direction.DOWN:
            return [(row, col-1, Direction.LEFT), (row, col+1, Direction.RIGHT)]
        elif direction == Direction.RIGHT or direction == Direction.LEFT:
            return [travel(row, col, direction)]

largest = 0
for start in chain(
    [(row, 0, Direction.RIGHT) for row in range(len(board))],
    [(row, len(board[0])-1, Direction.LEFT) for row in range(len(board))],
    [(0, col, Direction.DOWN) for col in range(len(board[0]))],
    [(len(board)-1, col, Direction.UP) for col in range(len(board[0]))]
):
    beams = deque()
    beams.append(start)

    energized = np.zeros((len(board), len(board[0])), dtype=np.bool_)
    seen = set()

    while len(beams) > 0:
        row, col, direction = beams.popleft()
        key = "{}|{}|{}".format(row, col, direction)
        if key in seen:
            continue
        seen.add(key)
        if row < 0 or row >= len(board) or col < 0 or col >= len(board[0]):
            continue
        energized[row, col] = True
        if board[row][col] == '.':
            beams.append(travel(row, col, direction))
        elif board[row][col] == '/':
            beams.append(bounce(row, col, direction, True))
        elif board[row][col] == '\\':
            beams.append(bounce(row, col, direction, False))
        elif board[row][col] == '|':
            beams.extend(youGotPiped(row, col, direction, True))
        elif board[row][col] == '-':
            beams.extend(youGotPiped(row, col, direction, False))
        else:
            raise RuntimeError('wat:' + board[row][col])

    largest = max(largest, np.sum(energized))

print(largest)