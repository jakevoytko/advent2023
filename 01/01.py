f = open('input.txt', 'r')

sum = 0

for line in f:
    numbers = [int(c) for c in line if c.isdigit()]
    sum += 10 * numbers[0] + numbers[-1]

print(sum)

f.close()
