import numpy as np

f = open('input.txt', 'r')

boards = [[]]
sum = 0

for line in f:
    if line != '\n' and line != '':
        boards[-1].append([*line.strip()])
        continue

    boards.append([])

f.close()

def reflection_score(board):
    for row in range(1, board.shape[0]):
        prefix = board[:row]
        suffix = board[row:]

        if prefix.shape[0] < suffix.shape[0]:
            suffix = suffix[:prefix.shape[0]]
        else:
            prefix = prefix[-suffix.shape[0]:]
        suffix = np.flip(suffix, axis = 0)
        xor = prefix != suffix
        if xor.sum() == 1:
            return row * 100
    
    for col in range(1, board.shape[1]):
        prefix = board[:, :col]
        suffix = board[:, col:]

        if prefix.shape[1] < suffix.shape[1]:
            suffix = suffix[:, :prefix.shape[1]]
        else:
            prefix = prefix[:, -suffix.shape[1]:]
        prefix = np.flip(prefix, axis = 1)
        xor = prefix != suffix
        if xor.sum() == 1:
            return col

for board in boards:
    board = np.array(board) == '#'
    sum += reflection_score(board)

print(sum)