import numpy as np
from functools import reduce

f = open('input.txt', 'r')

board = []

for line in f:
    board.append([*line.strip()])

f.close()

board = np.array(board) == '#'
expandRows = ~board.any(axis=1)
expandCols = ~board.any(axis=0)
def reduceFn(x, y):
    x.append(x[-1] + [0, 1][y])
    return x
rowExpansionMap = reduce(reduceFn, expandRows, [0])[1:]
colExpansionMap = reduce(reduceFn, expandCols, [0])[1:]

allPoints = [(y + colExpansionMap[y], x + rowExpansionMap[x]) for [x, y] in np.argwhere(board)]

def manhattanDistance(p0, p1):
    return abs(p1[0] - p0[0]) + abs(p1[1] - p0[1])

sum = 0

for i in range(len(allPoints)):
    for j in range(i + 1, len(allPoints)):
        sum += manhattanDistance(allPoints[i], allPoints[j])

print(sum)