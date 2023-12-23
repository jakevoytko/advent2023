from collections import deque
f = open('input.txt', 'r')

board = [[*line.strip()] for line in f]
f.close()

start = (0, 1)
end = (len(board) - 1, len(board[0]) - 2)

allSteps = deque([(start, set(start), 0)])

longest = -1

while len(allSteps) > 0:
    step, seen, numberOfSteps = allSteps.popleft()
    if step == end:
        longest = max(longest, numberOfSteps)

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    if board[step[0]][step[1]] == '<':
        directions = [(0, -1)]
    elif board[step[0]][step[1]] == '>':
        directions = [(0, 1)]
    elif board[step[0]][step[1]] == '^':
        directions = [(-1, 0)]
    elif board[step[0]][step[1]] == 'v':
        directions = [(1, 0)]
    for direction in directions:
        nextStep = (step[0] + direction[0], step[1] + direction[1])
        if nextStep[0] < 0 or nextStep[0] >= len(board) or nextStep[1] < 0 or nextStep[1] >= len(board[0]):
            continue
        if nextStep not in seen and board[nextStep[0]][nextStep[1]] != '#':
            nextSeen = seen.copy()
            nextSeen.add(nextStep)
            allSteps.append((nextStep, nextSeen, numberOfSteps + 1))

print(longest)