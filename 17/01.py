import heapq
import enum

f = open('input.txt', 'r')

board = [[int(x) for x in [*line.strip()]] for line in f]
f.close()

class Direction(enum.Enum):
  UP = 1
  DOWN = 2
  LEFT = 3
  RIGHT = 4

  def __lt__(self, other):
    return self.value < other.value

q = [(-board[0][0], 0, 0, Direction.DOWN, 0, None)]
minMap = {}

directionMap = {
  Direction.UP: [(-1, 0, Direction.UP, True), (0, -1, Direction.LEFT, False), (0, 1, Direction.RIGHT, False)],
  Direction.DOWN: [(1, 0, Direction.DOWN, True), (0, -1, Direction.LEFT, False), (0, 1, Direction.RIGHT, False)],
  Direction.LEFT: [(0, -1, Direction.LEFT, True), (-1, 0, Direction.UP, False), (1, 0, Direction.DOWN, False)],
  Direction.RIGHT: [(0, 1, Direction.RIGHT, True), (-1, 0, Direction.UP, False), (1, 0, Direction.DOWN, False)],
}

while len(q) > 0:
  last = heapq.heappop(q)
  cost, row, col, direction, pathLength, path = last
  cost = cost + board[row][col]

  if row == len(board) - 1 and col == len(board[0]) - 1:
    print(cost)
    break
  key = "{}-{}-{}-{}".format(row, col, direction.value, pathLength)
  if key in minMap:
    if cost >= minMap[key]:
      continue
  minMap[key] = cost

  for (rowOffset, colOffset, newDirection, continuation) in directionMap[direction]:
    next = (cost, row + rowOffset, col + colOffset, newDirection, [1, pathLength + 1][continuation], last)
    if next[4] <= 3 and (next[1] >= 0 and next[1] < len(board) and next[2] >= 0 and next[2] < len(board[0])):
      heapq.heappush(q, next)
