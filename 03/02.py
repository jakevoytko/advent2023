f = open('input.txt', 'r')

board = []

for line in f:
    board.append([*line.strip()])

f.close()

def findAndScrub(board, row, col):
    if row < 0 or row >= len(board) or col < 0 or col >= len(board[row]):
        return None
    if not board[row][col].isdigit():
        return None
    
    current = ''

    coliter = col

    while coliter >= 0 and board[row][coliter].isdigit():
        current = board[row][coliter] + current
        board[row][coliter] = '.'
        coliter -= 1
    
    coliter = col + 1
    while coliter < len(board[row]) and board[row][coliter].isdigit():
        current = current + board[row][coliter]
        board[row][coliter] = '.'
        coliter += 1

    if current == '':
        return None
    
    return int(current)

directions = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]

total = 0

for row in range(0, len(board)):
    for col in range(0, len(board[row])):
        if board[row][col] != '*':
            continue

        boardclone = [row[:] for row in board]

        numbers = []
        for direction in directions:
            result = findAndScrub(boardclone, row+direction[0], col+direction[1])
            if result is not None:
                numbers.append(result)
        if len(numbers) == 2:
            total += numbers[0] * numbers[1]

print(total)