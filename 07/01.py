from collections import defaultdict
from enum import Enum

f = open('input.txt', 'r')

class HandClass(Enum):
  HIGH_CARD = 1
  ONE_PAIR = 2
  TWO_PAIR = 3
  THREE_OF_A_KIND = 4
  FULL_HOUSE = 5
  FOUR_OF_A_KIND = 6
  FIVE_OF_A_KIND = 7

  def __lt__(self, other):
    return self.value < other.value

cardValues = {
  'A': 14,
  'K': 13,
  'Q': 12,
  'J': 11,
  'T': 10,
  '9': 9,
  '8': 8,
  '7': 7,
  '6': 6,
  '5': 5,
  '4': 4,
  '3': 3,
  '2': 2
}
    

def classify(hand):
  counts = defaultdict(int)
  for card in hand:
    counts[card] = counts[card] + 1
  
  if len(counts) == 1:
    return HandClass.FIVE_OF_A_KIND
  
  sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
  if len(counts) == 2:
    if sorted_counts[0][1] == 4:
      return HandClass.FOUR_OF_A_KIND
    else:
      return HandClass.FULL_HOUSE
  
  if len(counts) == 3:
    if sorted_counts[0][1] == 3:
      return HandClass.THREE_OF_A_KIND
    else:
      return HandClass.TWO_PAIR
  
  if len(counts) == 4:
    return HandClass.ONE_PAIR
  
  return HandClass.HIGH_CARD


hands = [([a for a in map(lambda x: cardValues[x], hand)], int(bid)) for hand, bid in [line.strip().split(' ') for line in f]]
classified_hands = [(classify(hand), hand, bid) for hand, bid in hands]
sorted_hands = [x for x in sorted(classified_hands)]
winnings = 0
for i in range(0, len(sorted_hands)):
  hand = sorted_hands[i]
  bid = hand[2]
  winnings += (i + 1) * bid

print(winnings)

f.close()
