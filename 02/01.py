import re

f = open('input.txt', 'r')

sum = 0

gamePattern = re.compile(r'Game (\d+)')
cubePattern = re.compile(r'(\d+) (\w+)')

for line in f:
    gameString, setString = line.split(':')
    game = int(gamePattern.search(gameString).group(1))

    possible = True

    for set in setString.split(';'):
        cubes = set.split(',')
        for cube in cubes:
            match = cubePattern.search(cube)
            cubeCount = int(match.group(1))
            cubeColor = match.group(2)
            if cubeColor == 'red' and cubeCount > 12 or cubeColor == 'green' and cubeCount > 13 or cubeColor == 'blue' and cubeCount > 14:
                possible = False
                break
        if not possible:
            break
    
    if possible:
        sum += game

print(sum)

f.close()
