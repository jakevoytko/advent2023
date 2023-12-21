from functools import reduce
import re
from collections import deque, defaultdict

f = open('input.txt', 'r')

class BroadcasterModule:
    def __init__(self, label, destinations):
        self.label = label
        self.destinations = destinations
        self.inputLength = 0

    def process(self, origin, isHigh):
        return [(destination, self.label, isHigh) for destination in self.destinations]
        
    def __repr__(self):
        return "[type: Broadcaster, label: {}, destinations: {}]".format(self.label, self.destinations)

    def isOriginState(self):
        return self.inputLength == 0

class FlipFlopModule:
    def __init__(self, label, destinations):
        self.label = label
        self.destinations = destinations
        self.memory = False
        self.inputLength = 0

    def process(self, origin, isHigh):
        if isHigh:
            return []
        self.memory = not self.memory
        return [(destination, self.label, self.memory) for destination in self.destinations]
    
    def setOrigins(self, origins):
        self.memory = {origin: False for origin in origins}

    def __repr__(self):
        return "[type: FlipFlop, label: {}, destinations: {}, memory: {}]".format(self.label, self.destinations, self.memory)

    def isOriginState(self):
        return self.memory == False and self.inputLength == 0


class ConjunctionModule():
    def __init__(self, label, destinations):
        self.label = label
        self.destinations = destinations
        self.memory = None
        self.inputLength = 0
    
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

    def isOriginState(self):
        for origin in self.memory:
            if self.memory[origin]:
                return False
        return self.inputLength == 0

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

def allModuleParents(moduleOrigins, label):
    parents = set()
    queue = deque([label])
    while len(queue) > 0:
        l = queue.popleft()
        parents.add(l)
        for origin in moduleOrigins[l]:
            if origin not in parents:
                queue.append(origin)
    return parents

moduleParents = {}

for label, module in modules.items():
    parents = allModuleParents(moduleOrigins, label)
    if len(parents) > 0:
        moduleParents[label] = parents

def isTransitiveClosureOriginState(modules, generators, moduleParents, destination):
    allOrigin = True
    if destination == 'rx':
        return False
    for parent in moduleParents[destination]:
        if parent in generators:
            if not generators[parent].isOriginState():
                allOrigin = False
                break
        elif parent in modules:
            if not modules[parent].isOriginState():
                allOrigin = False
                break
        # else it is a module that is no longer needed for processing, ignore
    return allOrigin


class Generator:
    def __init__(self, label, history, cycleLength, destinations):
        self.label = label
        self.history = history
        self.cycleLength = cycleLength
        self.destinations = destinations
        self.iteration = 1
        self.offset = 0
    
    def peekNextButtonPress(self):
        return (self.label, self.cycleLength * self.iteration + self.history[self.offset][0])

    def advance(self):
        next = self.history[self.offset]
        retVal = (self.iteration * self.cycleLength + next[0], next[1])
        self.offset += 1
        if self.offset == len(self.history):
            self.offset = 0
            self.iteration += 1
        return retVal

    def isOriginState(self):
        return self.offset == 0

    def destinations(self):
        return self.destinations

generators = {
    'button': Generator('button', [(0, False)], 1, ['broadcaster']),
}
labelHistory = defaultdict(list)

currentButtonPress = 0
removingIndices = set()

while len(removingIndices) < 5:
    nextButtonPress = 2**256
    nextLabel = None
    for l in generators:
        generator = generators[l]
        genLabel, genPress = generator.peekNextButtonPress()
        if genPress < nextButtonPress:
            nextButtonPress = genPress
            nextLabel = genLabel
        nextButtonPress = min(nextButtonPress, genPress)
    currentButtonPress, next = generators[nextLabel].advance()

    signals = deque()
    for dest in generators[nextLabel].destinations:
        signals.append((dest, nextLabel, next))
        if dest in modules:
            modules[dest].inputLength += 1

    while len(signals) > 0:
        (destination, origin, isHigh) = signals.popleft()
        if destination in modules:
            modules[destination].inputLength -= 1

        if destination in modules:
            processed = modules[destination].process(origin, isHigh)
            if len(processed) > 0:
                labelHistory[destination].append((currentButtonPress, processed[0][2]))
            signals.extend(processed)
            for (d, ignore, ignore) in processed:
                if d != 'rx':
                    modules[d].inputLength += 1

        if isTransitiveClosureOriginState(modules, generators, moduleParents, destination):
            for parent in moduleParents[destination]:
                if parent in modules:
                    module = modules[parent]
                    del[modules[parent]]
                    generator = Generator(parent, labelHistory[parent], currentButtonPress, module.destinations)
                    generators[parent] = generator
        
            # Look for generators whose destinations are all in generators and remove them
            toRemove = []
            for label in generators:
                generator = generators[label]
                if all([dest not in modules for dest in generator.destinations]):
                    removingIndices.add(currentButtonPress)
                    toRemove.append(label)
            for label in toRemove:
                del[generators[label]]

# The final octopus merge prints true every turn except for 1 in a few thousand. When
# all 4 are false on the same round, that button turn is the answer. It happens to line
# up with 4 full cycles of the button generator, so we can just multiply those together and
# call it a day.
# removingIndices also has button being removed at 1, but that doesn't change the output.
print(reduce(lambda x, y: x * y, removingIndices, 1))
