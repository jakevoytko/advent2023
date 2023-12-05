from functools import reduce

f = open('input.txt', 'r')

seedLine = f.readline()
seeds = set([int(c) for c in seedLine.split(' ')[1:] if c != ''])
f.readline()

expectingNewConversion = True

newSeeds = set()
for line in f:
    if expectingNewConversion:
        expectingNewConversion = False
        continue
    
    if line == '\n':
        expectingNewConversion = True
        for seed in seeds:
            newSeeds.add(seed)
        seeds = newSeeds
        newSeeds = set()
        continue

    destStart, sourceStart, num = [int(x) for x in line.strip().split(' ') if x != '']
    sourceEnd = sourceStart + num
    removed = set()
    for seed in seeds:
        if seed >= sourceStart and seed < sourceEnd:
            newSeeds.add(destStart + seed - sourceStart)
            removed.add(seed)
    for seed in removed:
        seeds.remove(seed)

for seed in seeds:
    newSeeds.add(seed)
seeds = newSeeds

print(reduce(lambda a, b: min(a, b), seeds, 2**256))

f.close()
