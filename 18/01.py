import re
import numpy as np

f = open('input.txt', 'r')

orders = []

lineRegex = re.compile(r'(\w) (\d+) \((#[0-9a-f]+)\)')
seen = {}
current = (0, 0)
def markSeen(seen, current):
    seen[current] = True

directionMap = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
}

for line in f:
    match = lineRegex.search(line.strip())
    direction = match.group(1)
    distance = int(match.group(2))
    color = match.group(3)
  
    for i in range(distance):
        current = (current[0] + directionMap[direction][0], current[1] + directionMap[direction][1])
        markSeen(seen, current)

f.close()

minRow = 2**128
maxRow = -1
minCol = 2**128
maxCol = -1

for (row, col) in seen:
    minRow = min(minRow, row)
    maxRow = max(maxRow, row)
    minCol = min(minCol, col)
    maxCol = max(maxCol, col)

board = np.full((maxRow - minRow + 1, maxCol - minCol + 1), '.')
for (row, col) in seen:
    board[row - minRow][col - minCol] = '#'

def floodFill(board, row, col):
    queue = [(row, col)]
    while len(queue):
        r, c = queue.pop()
        if board[r, c] == '#':
            continue
        board[r, c] = '#'
        queue.append((r - 1, c))
        queue.append((r + 1, c))
        queue.append((r, c - 1))
        queue.append((r, c + 1))

floodFill(board, 22, 88) # if you're not cheating, you're not trying
print((board == '#').sum())