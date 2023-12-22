import re

f = open('input.txt', 'r')

bricks = []

class Coordinate:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))
    
    def __eq__(self, o):
        return self.x == o.x and self.y == o.y and self.z == o.z

class Brick:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        if self.start.x > self.end.x or self.start.y > self.end.y or self.start.z > self.end.z:
            self.start, self.end = self.end, self.start

        self.xyBlocks = set()
        for x in range(start.x, end.x + 1):
            for y in range(start.y, end.y + 1):
                self.xyBlocks.add((x, y))
      
    def intersectsXY(self, other):
        return len(self.xyBlocks.intersection(other.xyBlocks)) > 0
  
    def supports(self, other):
        return self.end.z == (other.start.z - 1) and self.intersectsXY(other)

    def __repr__(self):
        return f'({self.start}, {self.end})'
    
    def moveBottomToHeight(self, height):
        delta = self.start.z - height
        self.start.z -= delta
        self.end.z -= delta
    
    def clone(self):
        return Brick(Coordinate(self.start.x, self.start.y, self.start.z), Coordinate(self.end.x, self.end.y, self.end.z))

    def __hash__(self):
        return hash((self.start, self.end))
    
    def __eq__(self, o):
        return self.start == o.start and self.end == o.end

brickRegex = re.compile(r'(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)')
for line in f:
    match = brickRegex.search(line)
    bricks.append(Brick(Coordinate(int(match.group(1)), int(match.group(2)), int(match.group(3))), Coordinate(int(match.group(4)), int(match.group(5)), int(match.group(6)))))
f.close()

# Sort bricks by their min point.
bricks = sorted(bricks, key=lambda brick: (brick.start.z, brick.start.x, brick.start.y))

# MAKE IT RAIN
for i, brick in enumerate(bricks):
  restingHeight = None
  for fallenBrick in bricks[:i]:
    if brick.intersectsXY(fallenBrick) and fallenBrick.end.z < brick.start.z:
      if restingHeight is None or (fallenBrick.end.z + 1) > restingHeight:
        restingHeight = fallenBrick.end.z + 1
  if restingHeight is None:
      brick.moveBottomToHeight(1)
  else:
      brick.moveBottomToHeight(restingHeight)

# resort because stuff fell
bricks = sorted(bricks, key=lambda brick: (brick.start.z, brick.start.x, brick.start.y))

# MAKE IT RAIN A LOT MORE
count = 0
for i in range(len(bricks)):
    bricksWithoutBrick = [b.clone() for b in (bricks[:i] + bricks[i + 1:])]

    for j, brick in enumerate(bricksWithoutBrick):
        restingHeight = None
        for fallenBrick in bricksWithoutBrick[:j]:
            if brick.intersectsXY(fallenBrick) and fallenBrick.end.z < brick.start.z:
                if restingHeight is None or (fallenBrick.end.z + 1) > restingHeight:
                    restingHeight = fallenBrick.end.z + 1
        if restingHeight is None:
            if brick.start.z != 1:
                count+=1
            brick.moveBottomToHeight(1)
        else:
            if brick.start.z != restingHeight:
                count+=1
            brick.moveBottomToHeight(restingHeight)

    print(i, count)

print(count)