f = open('input.txt', 'r')

times = [int(c) for c in f.readline().split(' ')[1:] if c != '']
records = [int(c) for c in f.readline().split(' ')[1:] if c != '']

f.close()

races = zip(times, records)

sum = 1

for time, record in races:
    ways = 0
    for i in range(time):
        remaining = time - i
        speed = i
        distance = speed * remaining
        if distance > record:
            ways += 1
    sum *= ways

print(sum)