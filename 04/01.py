f = open('input.txt', 'r')

sum = 0

for line in f:
    prefix, suffix = line.split(':')
    winning, have = suffix.split('|')
    allWinning = set([c.strip() for c in winning.split(' ') if c.strip() != ''])
    allHave = [c.strip() for c in have.split(' ') if c.strip() != '' and c.strip() in allWinning]
    if len(allHave) > 0:
        sum += 2**(len(allHave) - 1)

print(sum)

f.close()
