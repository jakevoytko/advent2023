import re

f = open('input.txt', 'r')

instructions = f.readline().strip()
f.readline() # empty line in input

instructionMap = {}

expression = re.compile(r'(\w\w\w) = \((\w\w\w), (\w\w\w)\)')

for line in f:
  m = expression.match(line)
  instructionMap[m.group(1)] = (m.group(2), m.group(3))

f.close()

current = 'AAA'
index = 0
count = 0

while current != 'ZZZ':
  count += 1
  instruction = instructionMap[current]
  if instructions[index] == 'L':
    current = instruction[0]
  else:
    current = instruction[1]
  index = (index + 1) % len(instructions)

print(count)