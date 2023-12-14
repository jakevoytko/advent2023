import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)

f = open('input.txt', 'r')

charBoard = []

for line in f:
    charBoard.append([*line.strip()])

f.close()

charBoard = np.array(charBoard)
board = np.zeros_like(charBoard, dtype = np.int32)
board[charBoard == '#'] = 1
board[charBoard == 'O'] = 2

count = 0
seenHash = {}
boards = {}
seenAt = None
seenValue = None

while(True):
    for row, col in np.argwhere(board == 2):
        # up 
        all = np.argwhere(board[:row,col] > 0)
        board[row][col] = 0
        if len(all) == 0:
            board[0][col] = 2
        else:
            board[all[-1][0] + 1][col] = 2

    for row, col in np.argwhere(board == 2):
        # left
        all = np.argwhere(board[row, :col] > 0)
        board[row][col] = 0
        if len(all) == 0:
            board[row][0] = 2
        else:
            board[row][all[-1][0] + 1] = 2

    for row, col in np.flip(np.argwhere(board == 2), axis=0):
        # down
        all = np.argwhere(board[row+1:,col] > 0)
        board[row][col] = 0
        if len(all) == 0:
            board[-1][col] = 2
        else:
            board[row + all[0][0]][col] = 2
    
    for row, col in np.flip(np.argwhere(board == 2), axis=0):
        # right
        all = np.argwhere(board[row,col+1:] > 0)
        board[row][col] = 0
        if len(all) == 0:
            board[row][-1] = 2
        else:
            board[row][col + all[0][0]] = 2

    count += 1
    key = np.array2string(board, separator='', max_line_width = None)
    if key in seenHash:
        seenAt = count
        seenValue = seenHash[key]
        break

    seenHash[key] = count
    boards[count] = board.copy()

target = 1000000000 - seenValue
loopLength = seenAt - seenValue
loopIter = target - (target // loopLength) * loopLength
finalBoard = boards[loopIter + seenValue]
print(np.sum(np.arange(finalBoard.shape[0], 0, -1) * (finalBoard == 2).sum(axis = 1)))
