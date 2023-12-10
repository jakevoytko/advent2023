from collections import deque

f = open('input.txt', 'r')

board = []

for line in f:
    board.append([*line.strip()])

f.close()

start = (-1, -1)

for row in range(len(board)):
    for col in range(len(board[row])):
        if board[row][col] == 'S':
            start = (row, col)

queue = deque([(start, 0)])

furthest = 0
seen = set()

while len(queue) > 0:
    next, count = queue.popleft()
    row, col = next
    char = board[next[0]][next[1]]
    if next in seen or next[0] < 0 or next[0] >= len(board) or next[1] < 0 or next[1] >= len(board[row]) or char == '.':
        continue
    seen.add(next)
    furthest = max(count, furthest)
    board[row][col] = '!'

    if char == '|':
        queue.append(((row - 1, col), count + 1))
        queue.append(((row + 1, col), count + 1))
    elif char == '-':
        queue.append(((row, col - 1), count + 1))
        queue.append(((row, col + 1), count + 1))
    elif char == 'L':
        queue.append(((row - 1, col), count + 1))
        queue.append(((row, col + 1), count + 1))
    elif char == 'J':
        queue.append(((row - 1, col), count + 1))
        queue.append(((row, col - 1), count + 1))
    elif char == '7':
        queue.append(((row + 1, col), count + 1))
        queue.append(((row, col - 1), count + 1))
    elif char == 'F':
        queue.append(((row + 1, col), count + 1))
        queue.append(((row, col + 1), count + 1))
    elif char == 'S':
        if board[row - 1][col] == '|' or board[row-1][col] == '7' or board[row-1][col] == 'F':
            queue.append(((row - 1, col), count + 1))
        if board[row + 1][col] == '|' or board[row+1][col] == 'L' or board[row+1][col] == 'J':
            queue.append(((row + 1, col), count + 1))
        if board[row][col - 1] == '-' or board[row][col-1] == 'F' or board[row][col-1] == 'L':
            queue.append(((row, col - 1), count + 1))
        if board[row][col + 1] == '-' or board[row][col-1] == 'J' or board[row][col-1] == '7':
            queue.append(((row, col + 1), count + 1))

print(furthest)