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

queue = deque([start])

seen = set()

while len(queue) > 0:
    next = queue.popleft()
    row, col = next
    char = board[next[0]][next[1]]
    if next in seen or next[0] < 0 or next[0] >= len(board) or next[1] < 0 or next[1] >= len(board[row]) or char == '.':
        continue
    seen.add(next)

    if char == '|':
        queue.append((row - 1, col))
        queue.append((row + 1, col))
    elif char == '-':
        queue.append((row, col - 1))
        queue.append((row, col + 1))
    elif char == 'L':
        queue.append((row - 1, col))
        queue.append((row, col + 1))
    elif char == 'J':
        queue.append((row - 1, col))
        queue.append((row, col - 1))
    elif char == '7':
        queue.append((row + 1, col))
        queue.append((row, col - 1))
    elif char == 'F':
        queue.append((row + 1, col))
        queue.append((row, col + 1))
    elif char == 'S':
        up = False
        down = False
        right = False
        left = False
        if board[row - 1][col] == '|' or board[row-1][col] == '7' or board[row-1][col] == 'F':
            queue.append((row - 1, col))
            up = True
        if board[row + 1][col] == '|' or board[row+1][col] == 'L' or board[row+1][col] == 'J':
            queue.append((row + 1, col))
            down = True
        if board[row][col - 1] == '-' or board[row][col-1] == 'F' or board[row][col-1] == 'L':
            queue.append((row, col - 1))
            left = True
        if board[row][col + 1] == '-' or board[row][col-1] == 'J' or board[row][col-1] == '7':
            queue.append((row, col + 1))
            right = True
        
        # Replace the start character with the appropriate pipe character
        if up and down:
            board[row][col] = '|'
        elif left and right:
            board[row][col] = '-'
        elif up and right:
            board[row][col] = 'L'
        elif up and left:
            board[row][col] = 'J'
        elif down and right:
            board[row][col] = 'F'
        elif down and left:
            board[row][col] = '7'

# Create an orientation map indicating what direction from each pipe segment is inside the pipe
def makeInsideMap(board, seen):
    insideMap = {}
    seen2 = set()
    for row in range(len(board)):
        for col in range(len(board[row])):
            if (row, col) not in seen or board[row][col] != '|':
                continue

            queue = deque([((row, col), 'r')])
            while len(queue) > 0:
                next, direction = queue.popleft()
                r, c = next
                char = board[r][c]
                if next in seen2:
                    continue
                seen2.add(next)
                insideMap[next] = direction

                if char == '|':
                    queue.append(((r - 1, c), direction))
                    queue.append(((r + 1, c), direction))
                elif char == '-':
                    queue.append(((r, c - 1), direction))
                    queue.append(((r, c + 1), direction))
                elif char == 'L':
                    queue.append(((r - 1, c), 'l' if direction == 'd' else 'r'))
                    queue.append(((r, c + 1), 'd' if direction == 'l' else 'u'))
                elif char == 'J':
                    queue.append(((r - 1, c), 'l' if direction == 'u' else 'r'))
                    queue.append(((r, c - 1), 'u' if direction == 'l' else 'd'))
                elif char == '7':
                    queue.append(((r + 1, c), 'r' if direction == 'u' else 'l'))
                    queue.append(((r, c - 1), 'u' if direction == 'r' else 'd'))
                elif char == 'F':
                    queue.append(((r + 1, c), 'r' if direction == 'd' else 'l'))
                    queue.append(((r, c + 1), 'd' if direction == 'r' else 'u'))
            return insideMap

insideMap = makeInsideMap(board, seen)

count = 0
runCount = 0
lastDirection = None
for row in range(len(board)):
    for col in range(len(board[row])):
        boardChar = board[row][col]
        if (row, col) in seen:
            if lastDirection == 'r':
                count += runCount
            lastDirection = insideMap[(row, col)]
            if lastDirection == 'd' and boardChar == 'J' or lastDirection == 'u' and boardChar == '7':
                lastDirection = 'r'
            runCount = 0
        else:
            runCount += 1

print(count)
