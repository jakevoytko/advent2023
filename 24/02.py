import re
import numpy as np
import sympy as sp

f = open('input.txt', 'r')

class Coordinate:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'

class BoundingBox:
    def __init__(self, min, max):
        self.min = min
        self.max = max
    
    def __repr__(self):
        return f'BoundingBox({self.min}, {self.max})'

    def __contains__(self, o):
        return self.min.x <= o.x <= self.max.x and self.min.y <= o.y <= self.max.y and self.min.z <= o.z <= self.max.z
      
hail = []

hailRegex = re.compile(r'([0-9-]+), +([0-9-]+), +([0-9-]+) +@ +([0-9-]+), +([0-9-]+), +([0-9-]+)')
for line in f:
    match = hailRegex.search(line)
    hail.append((Coordinate(int(match.group(1)), int(match.group(2)), int(match.group(3))), Coordinate(int(match.group(4)), int(match.group(5)), int(match.group(6)))))
f.close()

count = 0

x, y, z, dx, dy, dz = sp.symbols('x y z dx dy dz')
equations = []
symbols = [x, y, z, dx, dy, dz]

for i, a in enumerate(hail[:3]):
    t1 = sp.symbols(f't{i}')
    equations.append(sp.Eq(x + dx * t1, a[0].x + a[1].x * t1))
    equations.append(sp.Eq(y + dy * t1, a[0].y + a[1].y * t1))
    equations.append(sp.Eq(z + dz * t1, a[0].z + a[1].z * t1))
    symbols.append(t1)

result = sp.solvers.solve(equations)
print(result[0][x] + result[0][y] + result[0][z])