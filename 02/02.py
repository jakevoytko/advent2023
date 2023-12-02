import re
from collections import defaultdict

f = open('input.txt', 'r')

sum = 0

cubePattern = re.compile(r'(\d+) (\w+)')

for line in f:
    gameString, setString = line.split(':')

    cubeConstraint = defaultdict(lambda: 0)
    for set in setString.split(';'):
        cubes = set.split(',')
        for cube in cubes:
            match = cubePattern.search(cube)
            cubeCount = int(match.group(1))
            cubeColor = match.group(2)

            cubeConstraint[cubeColor] = max(cubeConstraint[cubeColor], cubeCount)
    
    power = cubeConstraint['red'] * cubeConstraint['green'] * cubeConstraint['blue']
    sum += power
    
print(sum)

f.close()
