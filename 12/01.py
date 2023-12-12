f = open('input.txt', 'r')

def score(springs):
  ret = []
  contiguous = 0
  for i in range(len(springs)):
    if springs[i] == '#':
      contiguous += 1
    elif contiguous > 0:
      ret.append(contiguous)
      contiguous = 0
  return ret

def matches(wildcard, reified):
  for i in range(len(wildcard)):
    if wildcard[i] == '.' and reified[i] == '#' or wildcard[i] == '#' and reified[i] == '.':
      return False
  return True

def prepend_all(prepend, springs):
  if springs is None:
    return []
  ret = []
  for s in springs:
    ret.append(prepend + s)
  return ret

# I'm not here to make friends.
def all_configurations(remaining, contiguous):
  # Base cases
  if remaining < 0:
    return None
  if len(contiguous) == 0:
    return ['.' * remaining]
  elif contiguous[0] > remaining:
    return None

  next = contiguous[1:]
  ret = []
  for i in range(remaining):
    prefix = '.' * i + '#' * contiguous[0]
    if remaining == len(prefix) and len(next) == 0:
      ret.append(prefix)
    else:
      ret.extend(prepend_all(prefix + '.', all_configurations(remaining - i - contiguous[0] - 1, next)))

  return ret  

total = 0

for line in f:
  springs, contiguous = line.strip().split(' ')
  contiguous = [int(c) for c in contiguous.split(',')]
  for c in all_configurations(len(springs), contiguous):
    if matches(springs, c):
      total += 1

print(total)

f.close()
