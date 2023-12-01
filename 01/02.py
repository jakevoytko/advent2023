import regex

f = open('input.txt', 'r')

sum = 0

submap = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '0': 0,
}

forwardpattern = regex.compile(r'(one|two|three|four|five|six|seven|eight|nine|\d)')
backwardpattern = regex.compile(r'(?r)(one|two|three|four|five|six|seven|eight|nine|\d)')

for line in f:
    sum += 10 * submap[forwardpattern.search(line).group(1)] + submap[backwardpattern.search(line).group(1)]

print(sum)

f.close()
