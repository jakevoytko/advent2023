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
  'J': 1,
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

# Best hand that can be created with a joker given the bucket counts.
non_joker_best_hand_map = {
  tuple(): HandClass.FIVE_OF_A_KIND,
  tuple([1]): HandClass.FIVE_OF_A_KIND,
  tuple([2]): HandClass.FIVE_OF_A_KIND,
  tuple([3]): HandClass.FIVE_OF_A_KIND,
  tuple([4]): HandClass.FIVE_OF_A_KIND,
  tuple([5]): HandClass.FIVE_OF_A_KIND,
  (1, 1): HandClass.FOUR_OF_A_KIND,
  (2, 1): HandClass.FOUR_OF_A_KIND,
  (2, 2): HandClass.FULL_HOUSE,
  (3, 1): HandClass.FOUR_OF_A_KIND,
  (3, 2): HandClass.FULL_HOUSE,
  (4, 1): HandClass.FOUR_OF_A_KIND,
  (1, 1, 1): HandClass.THREE_OF_A_KIND,
  (2, 1, 1): HandClass.THREE_OF_A_KIND,
  (2, 2, 1): HandClass.TWO_PAIR,
  (3, 1, 1): HandClass.THREE_OF_A_KIND,
  (1, 1, 1, 1): HandClass.ONE_PAIR,
  (2, 1, 1, 1): HandClass.ONE_PAIR,
  (1, 1, 1, 1, 1): HandClass.HIGH_CARD,
}

def classify(hand):
  counts = defaultdict(int)
  for card in hand:
    if card != cardValues['J']:
      counts[card] = counts[card] + 1
  sorted_counts = sorted(counts.values(), reverse=True)
  return non_joker_best_hand_map[tuple(sorted_counts)]

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
