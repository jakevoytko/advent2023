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

brickRegex = re.compile(r'(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)')
for line in f:
    match = brickRegex.search(line)
    bricks.append(Brick(Coordinate(int(match.group(1)), int(match.group(2)), int(match.group(3))), Coordinate(int(match.group(4)), int(match.group(5)), int(match.group(6)))))
f.close()

# Sort bricks by their min point.
bricks = sorted(bricks, key=lambda brick: (brick.start.z, brick.start.x, brick.start.y))

# MAKE IT RAIN
count = 0
disintegrable = set(bricks)
for i, brick in enumerate(bricks):
  disintegrable.add(brick)
  restingHeight = None
  supportedBy = []
  for fallenBrick in bricks[:i]:
    if brick.intersectsXY(fallenBrick) and fallenBrick.end.z < brick.start.z:
      if restingHeight is None or (fallenBrick.end.z + 1) > restingHeight:
        restingHeight = fallenBrick.end.z + 1
        supportedBy = [fallenBrick]
      elif (fallenBrick.end.z + 1) == restingHeight:
        supportedBy.append(fallenBrick)
  if restingHeight is None:
      brick.moveBottomToHeight(1)
  else:
      brick.moveBottomToHeight(restingHeight)
  
  if len(supportedBy) == 1:
      for x in supportedBy:
          if x in disintegrable:
              disintegrable.remove(x)

print(len(disintegrable))