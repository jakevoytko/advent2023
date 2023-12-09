from functools import reduce
f = open('input.txt', 'r')

sum = 0

for line in f:
    numbers = [int(atom) for atom in line.strip().split(' ')]
    
    rows = [numbers]
    while not reduce(lambda a, b: a and (b == 0), rows[-1], True):
        newrow = []
        for i in range(len(rows[-1]) - 1):
            newrow.append(rows[-1][i + 1] - rows[-1][i])
        rows.append(newrow)
    val = 0
    for i in range(len(rows) - 1, -1, -1):
        val = rows[i][0] - val
    sum += val

print(sum)

f.close()
