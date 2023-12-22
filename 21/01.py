from collections import deque
f = open('input.txt', 'r')

board = [[*line] for line in f]
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

queue = deque()
queue.append((startRow, startCol, 0))
reachable = set()
seen = set()
while len(queue) > 0:
  row, col, distance = queue.popleft()

  if (row, col, distance) in seen:
    continue
  seen.add((row, col, distance))

  if row < 0 or row >= len(board) or col < 0 or col >= len(board[row]):
    continue
  elif board[row][col] == '#':
    continue

  if distance == 64:
    reachable.add((row, col))
    continue

  queue.append((row - 1, col, distance + 1))
  queue.append((row + 1, col, distance + 1))
  queue.append((row, col - 1, distance + 1))
  queue.append((row, col + 1, distance + 1))

print(len(reachable))