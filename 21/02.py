import numpy as np
import sys
from collections import deque
np.set_printoptions(threshold=sys.maxsize)

from collections import deque
f = open('input.txt', 'r')

board = [[*line.strip()] for line in f]
f.close()

startRow = None
startCol = None
for row, values in enumerate(board):
  for col, value in enumerate(values):
    if value == 'S':
      startRow = row
      startCol = col
      break
  if startRow is not None:
    break

board[startRow][startCol] = '.'

# Since the length of the board is odd in both directions, the pattern has a cycle
# of 2 in each direction.
board = np.array(board)
board = np.tile(board, (4, 4))

seen = set()
reachable = np.zeros_like(board, dtype=bool) # 🙄
queue = deque()
queue.append((startRow, startCol))
while len(queue) > 0:
  row, col = queue.popleft()

  if row < 0 or row >= board.shape[0] or col < 0 or col >= board.shape[1]:
    continue
  elif board[row, col] == '#':
    continue
  if (row, col) in seen:
    continue
  seen.add((row, col))

  reachable[row, col] = True

  queue.append((row - 1, col))
  queue.append((row + 1, col))
  queue.append((row, col - 1))
  queue.append((row, col + 1))

checkerboard = (np.indices(board.shape).sum(axis=0) % 2) == 1
# Get the parity right. Target is an odd number of steps, so the start is not a destination.
if checkerboard[startRow, startCol]:
  checkerboard = ~checkerboard

repeatingPattern = checkerboard & reachable
print(repeatingPattern[startRow][startCol])

target = 26501365

def manhattanDistance(row1, col1, row2, col2):
  return abs(row2 - row1) + abs(col2 - col1)

# Shift (row, col) by board's dimensions until it is above and to the left of startRow and startCol.
def normalize(board, row, col, startRow, startCol):
  while row >= startRow:
    row -= board.shape[0]
  while col >= startCol:
    col -= board.shape[1]
  return (row, col)

total = 0
# Determine how many times destination tiles appear within the bounds.
for row, col in np.argwhere(repeatingPattern):
  ##
  ## Calculate the total number of times this tile appears to the left of origin.
  row, col = normalize(board, row, col, startRow, startCol)

  remainingDistanceAbove = target - manhattanDistance(row, col, startRow, startCol)
  numberAbove = (remainingDistanceAbove + board.shape[0]) // board.shape[0]
  
  belowRow = row + board.shape[0]
  remainingDistanceBelow = target - manhattanDistance(belowRow, col, startRow, startCol)
  numberBelow = (remainingDistanceBelow + board.shape[0]) // board.shape[0]

  totalNumber = numberAbove + numberBelow
  # For each grid iteration, this tile appears one fewer times above and below. So calc
  # either the nth square if it is odd or the sum of the first n even numbers if it is even.
  if totalNumber % 2 == 1:
    total += ((totalNumber + 1) // 2)**2
  else:
    n = totalNumber // 2
    total += n * (n+1)

  ## 
  ## Calculate the total number of times this tile appears on (or to the right) of origin, adjusted
  ## for the altered tiling.
  col += board.shape[1]
  remainingDistanceAbove = target - manhattanDistance(row, col, startRow, startCol)
  numberAbove = (remainingDistanceAbove + board.shape[0]) // board.shape[0]
  
  belowRow = row + board.shape[0]
  remainingDistanceBelow = target - manhattanDistance(belowRow, col, startRow, startCol)
  numberBelow = (remainingDistanceBelow + board.shape[0]) // board.shape[0]

  totalNumber = numberAbove + numberBelow
  if totalNumber % 2 == 1:
    total += ((totalNumber + 1) // 2)**2
  else:
    n = totalNumber // 2
    total += n * (n+1)

print(total)
#                \
#                O\                         
#                 O                      
#                O                         
#                 O                        
#                S                          
