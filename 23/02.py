from collections import deque
f = open('input.txt', 'r')

board = [[*line.strip()] for line in f]
f.close()

start = (0, 1)
end = (len(board) - 1, len(board[0]) - 2)

allSteps = deque([(start, set(start), 0, None)])

longest = -1
longestSeen = -1

dirArr =  [(0, 1), (0, -1), (1, 0), (-1, 0)]
topArr = [(0, 1), (1, 0)]
bottomArr = [(0, 1), (-1, 0), (1, 0)]
leftArr = [(0, 1), (1, 0)]
rightArr = [(1, 0), (0, -1)]

# TODO if too slow, trim straightaways
while len(allSteps) > 0:
    step, seen, numberOfSteps, last = allSteps.popleft()
    if numberOfSteps > longestSeen:
        print(numberOfSteps, len(allSteps))
        longestSeen = numberOfSteps
    if step == end:
        longest = max(longest, numberOfSteps)
        continue

    directions = dirArr
    # Prune invalid paths based on loop closures
    if step[0] == 1: # Top row, can't go left or up.
        directions = topArr
    elif step[0] == len(board) - 2: # Bottom row, can't go left, can go down to finish.
        directions = bottomArr
    elif step[1] == 1: # Left column, can't go up or left.
        directions = leftArr
    elif step[1] == len(board[0]) - 2: # Right column, can't go right or up
        directions = rightArr
    toAdd = []
    for direction in directions:
        nextStep = (step[0] + direction[0], step[1] + direction[1])
        if nextStep == last:
            continue
        if nextStep[0] < 0 or nextStep[0] >= len(board) or nextStep[1] < 0 or nextStep[1] >= len(board[0]):
            continue
        if nextStep not in seen and board[nextStep[0]][nextStep[1]] != '#':
            toAdd.append((nextStep, seen.copy(), numberOfSteps + 1, step))
        
    for stepToAdd in toAdd:
        if len(toAdd) > 1:
            stepToAdd[1].add(step)
        allSteps.append(stepToAdd)

print(longest)