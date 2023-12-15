import re

f = open('input.txt', 'r')

def HASH(s):
    current_value = 0
    for c in s:
        code = ord(c)
        current_value = (17 * (current_value + code)) % 256
    return current_value

rooms = [[] for i in range(256)]
instruction_regex = re.compile(r'(\w+)([-=])(\d+)?')
for line in f:
    for particle in line.strip().split(','):
        instruction = instruction_regex.match(particle)
        label = instruction.group(1)
        label_hash = HASH(label)
        instruction_type = instruction.group(2)

        if instruction_type == '=':
            value = int(instruction.group(3))
            room_length = len(rooms[label_hash])
            acc = []
            found = False
            for lens in rooms[label_hash]:
                if lens[0] == label:
                    acc.append((label, value))
                    found = True
                else:
                    acc.append(lens)
            if not found:
                acc.append((label, value))
            rooms[label_hash] = acc
        else:
            rooms[label_hash] = [*filter(lambda x: x[0] != label, rooms[label_hash])]

f.close()

total = 0

for i, room in enumerate(rooms):
    for (slot, lens) in enumerate(room):
        total += (1 + i) * (1 + slot) * lens[1]

print(total)

