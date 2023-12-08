import re
from functools import reduce
from math import lcm

f = open('input.txt', 'r')

instructions = f.readline().strip()
f.readline() # empty line in input

instructionMap = {}

expression = re.compile(r'(\w\w\w) = \((\w\w\w), (\w\w\w)\)')

for line in f:
  m = expression.match(line)
  instructionMap[m.group(1)] = (m.group(2), m.group(3))

f.close()

def find_end(instructions, instructionMap, node):
  index = 0
  count = 0

  while not node.endswith('Z'):
    count += 1
    instruction = instructionMap[node]
    if instructions[index] == 'L':
      node = instruction[0]
    else:
      node = instruction[1]
    index = (index + 1) % len(instructions)
  return count

startNodes = [x for x in instructionMap.keys() if x.endswith('A')]
# Instruction length is 269 and all instructions are multiples of this. YOLO LCMd and it worked.
print(lcm(*[find_end(instructions, instructionMap, node) for node in startNodes]))