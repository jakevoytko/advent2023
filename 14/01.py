import numpy as np

f = open('input.txt', 'r')

charBoard = []

for line in f:
    charBoard.append([*line.strip()])

f.close()

charBoard = np.array(charBoard)
board = np.zeros_like(charBoard, dtype = np.int32)
board[charBoard == '#'] = 1
board[charBoard == 'O'] = 2

for row, col in np.argwhere(board == 2):
    all = np.argwhere(board[:row,col] > 0)
    board[row][col] = 0
    if len(all) == 0:
        board[0][col] = 2
    else:
        board[all[-1][0] + 1][col] = 2

print(np.sum(np.arange(board.shape[0], 0, -1) * (board == 2).sum(axis = 1)))
