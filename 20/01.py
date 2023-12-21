
import re
from collections import deque, defaultdict

f = open('input.txt', 'r')

class BroadcasterModule:
    def __init__(self, label, destinations):
        self.label = label
        self.destinations = destinations

    def process(self, origin, isHigh):
        return [(destination, self.label, isHigh) for destination in self.destinations]
        
    def __repr__(self):
        return "[type: Broadcaster, label: {}, destinations: {}]".format(self.label, self.destinations)

class FlipFlopModule:
    def __init__(self, label, destinations):
        self.label = label
        self.destinations = destinations
        self.memory = False

    def process(self, origin, isHigh):
        if isHigh:
            return []
        self.memory = not self.memory
        return [(destination, self.label, self.memory) for destination in self.destinations]
        
    def __repr__(self):
        return "[type: FlipFlop, label: {}, destinations: {}, memory: {}]".format(self.label, self.destinations, self.memory)

class ConjunctionModule():
    def __init__(self, label, destinations):
        self.label = label
        self.destinations = destinations
        self.memory = None
    
    def setOrigins(self, origins):
        self.memory = {origin: False for origin in origins}

    def process(self, origin, isHigh):
        self.memory[origin] = isHigh
        send = False
        for origin in self.memory:
            if not self.memory[origin]:
                send = True
                break
        return [(destination, self.label, send) for destination in self.destinations]
        
    def __repr__(self):
        return "[type: Conjunction, label: {}, destinations: {}, memory: {}]".format(self.label, self.destinations, self.memory)

modules = {}
moduleOrigins = defaultdict(list)

lineRegex = re.compile(r'([%&]?)(\w+) -> ([a-z, ]+)')
for line in f:
    match = lineRegex.match(line)
    if match is None:
        raise Exception('Invalid line: ' + line)

    type = match.group(1)
    label = match.group(2)
    destinations = match.group(3).split(', ')

    if type == '':
        modules[label] = BroadcasterModule(label, destinations)
    elif type == '%':
        modules[label] = FlipFlopModule(label, destinations)
    elif type == '&':
        modules[label] = ConjunctionModule(label, destinations)
    else:
        raise RuntimeError('Invalid type: ' + type)

    for destination in destinations:
        moduleOrigins[destination].append(label)

f.close()

for label, origins in moduleOrigins.items():
    if label in modules and isinstance(modules[label], ConjunctionModule):
        modules[label].setOrigins(origins)

lowSeen = 0
highSeen = 0
for i in range(0, 1000):
    signals = deque()
    signals.append(('broadcaster', 'button', False))

    while len(signals) > 0:
        (destination, origin, isHigh) = signals.popleft()
        if isHigh:
            highSeen += 1
        else:
            lowSeen += 1
        if destination not in modules:
            continue
        signals.extend(modules[destination].process(origin, isHigh))

print(lowSeen * highSeen)