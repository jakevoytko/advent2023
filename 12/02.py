from functools import cache

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


# I'm not here to make friends.
memo = {}
def all_configurations(springs, contiguous):
  cache_key = springs + str(contiguous)

  if cache_key in memo:
    return memo[cache_key]
  # Base cases
  if len(contiguous) == 0:
    if springs.find('#') == -1:
      memo[cache_key] = 1
      return 1
    memo[cache_key] = 0
    return 0
  min_length = sum(contiguous) + len(contiguous) - 1
  if min_length > len(springs):
    memo[cache_key] = 0
    return 0

  next = contiguous[1:]
  ret = 0
  for i in range(len(springs)):
    prefix = '.' * i + '#' * contiguous[0]
    if not matches(springs[:len(prefix)], prefix):
      continue
    if len(springs) == len(prefix) and len(next) == 0:
      ret += 1
    elif len(prefix) < len(springs) and springs[len(prefix)] != '#':
      ret += all_configurations(springs[len(prefix) + 1:], next)

  if cache_key is not None:
    memo[cache_key] = ret
  return ret  

total = 0

for line in f:
  springs, contiguous = line.strip().split(' ')
  springs = '?'.join([springs] * 5)
  contiguous = [int(c) for c in contiguous.split(',')]
  contiguous = contiguous * 5
  total += all_configurations(springs, contiguous)

print(total)

f.close()
