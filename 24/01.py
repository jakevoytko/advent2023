import re
import numpy as np

f = open('input.txt', 'r')

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f'({self.x}, {self.y})'

class BoundingBox:
    def __init__(self, min, max):
        self.min = min
        self.max = max
    
    def __repr__(self):
        return f'BoundingBox({self.min}, {self.max})'

    def __contains__(self, o):
        return self.min.x <= o.x <= self.max.x and self.min.y <= o.y <= self.max.y
      
hail = []

hailRegex = re.compile(r'([0-9-]+), +([0-9-]+), +([0-9-]+) +@ +([0-9-]+), +([0-9-]+), +([0-9-]+)')
for line in f:
    match = hailRegex.search(line)
    hail.append((Coordinate(int(match.group(1)), int(match.group(2))), Coordinate(int(match.group(4)), int(match.group(5)))))
f.close()

#boundingBox = BoundingBox(Coordinate(7, 7), Coordinate(27, 27))
boundingBox = BoundingBox(Coordinate(200000000000000, 200000000000000), Coordinate(400000000000000, 400000000000000))

def pathsIntersectAt(a, b):
    if a == b:
        return a
  
    aMat = np.array([
        [-a[1].x, b[1].x],
        [-a[1].y, b[1].y],
    ])
    bMat = np.array([
        [a[0].x - b[0].x],
        [a[0].y - b[0].y],
    ])
    
    try:
        answer = np.linalg.solve(aMat, bMat)
        s = answer[0]
        t = answer[1]
        if s < 0 or t < 0: # No negative time
            return None
        return Coordinate(a[0].x + a[1].x * s, a[0].y + a[1].y * s)
    except np.linalg.LinAlgError:
        return None

count = 0
for i, a in enumerate(hail):
    for b in hail[i + 1:]:
        intersection = pathsIntersectAt(a, b)
        if intersection is None:
            continue
        if intersection in boundingBox:
            count += 1

print(count)