from collections import deque

f = open('input.txt', 'r')

simulationCards = deque()
cardToWinningsMap = {}

for line in f:
    prefix, suffix = line.split(':')
    cardNumber = int(prefix.split(' ')[-1])
    winning, have = suffix.split('|')
    allWinning = set([c.strip() for c in winning.split(' ') if c.strip() != ''])
    haveCount = len([c.strip() for c in have.split(' ') if c.strip() != '' and c.strip() in allWinning])
    cardToWinningsMap[cardNumber] = [cardNumber + 1 + i for i in range(haveCount)]
    simulationCards.append(cardNumber)

f.close()

cardCount = 0

while len(simulationCards) > 0:
    cardCount+=1
    cardNumber = simulationCards.popleft()
    haveCount = len(cardToWinningsMap[cardNumber])

    for id in cardToWinningsMap[cardNumber]:
        simulationCards.append(id)

print(cardCount)
