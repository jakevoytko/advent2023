f = open('input.txt', 'r')

time = int(f.readline().strip().replace(' ', '').split(':')[1])
record = int(f.readline().strip().replace(' ', '').split(':')[1])

f.close()

start = 0
end = time - 1

def result(currentTime, totalTime):
    return currentTime * (totalTime - currentTime)

firstIndex = 0
lastIndex = 0

# Binary search 1: find the first index
while start < end:
    mid = (start + end) // 2

    current = result(mid, time)
    previous = result(mid - 1, time)

    # Case 1: mid is the answer
    if current > record and previous <= record:
        firstIndex = mid
        break
    
    # Case 2: mid is too low
    if current < record:
        start = mid + 1
        continue

    # Case 3: mid is too high
    if current > record:
        end = mid - 1
        continue


# Binary search 2: find the last index
start = 0
end = time - 1
while start < end:
    mid = (start + end) // 2

    current = result(mid, time)
    next = result(mid + 1, time)

    # Case 1: mid is the answer
    if current > record and next <= record:
        lastIndex = mid
        break
    
    # Case 2: mid is too high
    if current > record:
        start = mid + 1
        continue

    # Case 3: mid is too high
    if current < record:
        end = mid - 1
        continue

print(lastIndex - firstIndex + 1)