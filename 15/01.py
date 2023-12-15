f = open('input.txt', 'r')

def HASH(s):
    current_value = 0
    for c in s:
        code = ord(c)
        current_value = (17 * (current_value + code)) % 256
    return current_value

sum = 0

for line in f:
    for particle in line.strip().split(','):
        sum += HASH(particle)

f.close()

print(sum)

