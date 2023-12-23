import re

f = open('input.txt', 'r')

orders = []

lineRegex = re.compile(r'(\w) (\d+) \(#([0-9a-f]+)\)')
current = (0, 0)

def isVertical(segment):
    return segment[0][0] != segment[1][0]

def isHorizontal(segment):
    return not isVertical(segment)

directionMap = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
}

verticalLines = []
verticalOccasions = set()

for line in f:
    match = lineRegex.search(line.strip())
    garbage = match.group(1)
    garbage = int(match.group(2))
    hex = match.group(3)
    
    distance = int(hex[:5], 16)
    direction = ['R', 'D', 'L', 'U'][int(hex[5])]

    nextLineSegmentStart = current
    nextLineSegmentEnd = (current[0] + directionMap[direction][0] * distance, current[1] + directionMap[direction][1] * distance)
    current = nextLineSegmentEnd

    if isVertical((nextLineSegmentStart, nextLineSegmentEnd)):
        if nextLineSegmentStart[0] > nextLineSegmentEnd[0]:
            (nextLineSegmentStart, nextLineSegmentEnd) = (nextLineSegmentEnd, nextLineSegmentStart)
        verticalLines.append((nextLineSegmentStart, nextLineSegmentEnd))
        verticalOccasions.add(nextLineSegmentStart[0])
        verticalOccasions.add(nextLineSegmentEnd[0])

verticalLines.sort()

f.close()

total = 0

continuation = 0
lastRow = 0
for verticalOccasion in sorted(verticalOccasions):
    total += continuation * (verticalOccasion - lastRow)
    lastRow = verticalOccasion
    allIntersections = []
    toRemove = []
    for verticalLine in verticalLines:
        if verticalLine[1][0] < verticalOccasion:
            toRemove.append(verticalLine)
        if verticalLine[0][0] <= verticalOccasion <= verticalLine[1][0]:
            allIntersections.append(verticalLine)
    for verticalLine in toRemove:
        verticalLines.remove(verticalLine)
    allIntersections = [*sorted(allIntersections, key=lambda x: x[0][1])]
    parity = False
    lastCol = -1
    enteredAtTop = False
    enteredAtBottom = False
    leavingAtTop = False
    leavingAtBottom = False
    continuation = 0
    for intersection in allIntersections:
        # Top of a vertical line segment.
        if intersection[0][0] == verticalOccasion:
            if not parity:
                parity = True
                enteredAtTop = True
            else:
                if enteredAtTop:
                    enteredAtTop = False
                    continuation += intersection[0][1] - lastCol + 1
                    parity = False

                elif enteredAtBottom:
                    enteredAtBottom = False
                    total += intersection[0][1] - lastCol# + 1
                
                elif leavingAtTop:
                    leavingAtTop = False
                    total += intersection[0][1] - lastCol# + 1
                
                elif leavingAtBottom:
                    leavingAtBottom = False
                    continuation += intersection[0][1] - lastCol + 1
                    parity = False

                else:
                    leavingAtTop = True
                    continuation += intersection[0][1] - lastCol + 1
        
        # Bottom of a vertical line segment.
        elif intersection[1][0] == verticalOccasion:
            if not parity:
                parity = True
                enteredAtBottom = True

            else:
                if enteredAtBottom:
                    enteredAtBottom = False
                    total += intersection[0][1] - lastCol# + 1
                    parity = False

                elif enteredAtTop:
                    enteredAtTop = False
                    continuation += intersection[0][1] - lastCol# + 1

                elif leavingAtBottom:
                    leavingAtBottom = False
                    continuation += intersection[0][1] - lastCol# + 1

                elif leavingAtTop:
                    leavingAtTop = False
                    parity = False
                    total += intersection[0][1] - lastCol# + 1
                
                else:
                    leavingAtBottom = True
                    continuation += intersection[0][1] - lastCol# + 1

        else: # in the middle
            if parity:
                continuation += intersection[0][1] - lastCol + 1
            parity = not parity
        
        lastCol = intersection[0][1]

print(total + 1)