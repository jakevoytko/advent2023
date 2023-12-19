import re
from collections import deque

class Condition:
    def __init__(self, variable, operator, value):
        self.variable = variable
        self.operator = operator
        self.value = value
    
    def execute(self, xmas):
        value = None
        if self.variable == 'x':
            value = xmas.x
        elif self.variable == 'm':
            value = xmas.m
        elif self.variable == 'a':
            value = xmas.a
        elif self.variable == 's':
            value = xmas.s
        
        if self.operator == '<':
            return value < self.value
        elif self.operator == '>':
            return value > self.value
        raise Exception('Invalid operator: ' + self.operator)
    
    def negation(self):
        if self.operator == '<':
            return Condition(self.variable, '>', self.value - 1)
        elif self.operator == '>':
            return Condition(self.variable, '<', self.value + 1)
        raise Exception('Invalid operator: ' + self.operator)

    def strip(self, rangeMap):
        values = rangeMap[self.variable]
        newValues = []
        for value in values:
            if self.operator == '<':
                if value.end < self.value:
                    continue
                elif value.start < self.value:
                    newValues.append(Range(value.start, self.value - 1))
            elif self.operator == '>':
                if value.start > self.value:
                    continue
                elif value.end > self.value:
                    newValues.append(Range(self.value + 1, value.end))
        rangeMap[self.variable] = newValues

    def __repr__(self):
        return self.variable + self.operator + str(self.value)

class Instruction:
    def __init__(self, condition, destination):
        self.condition = condition
        self.destination = destination
    
    def execute(self, xmas):
        if self.condition is None:
            return self.destination
    
        result = self.condition.execute(xmas)
        if result:
            return self.destination

        return None

    def __repr__(self):
        return str(self.condition) + ' -> ' + self.destination

class Rule:
    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions
    
    def execute(self, xmas):
        for instruction in self.instructions:
            result = instruction.execute(xmas)
            if result is not None:
                return result
        return None

    def __repr__(self):
        return self.name + "||" + str(self.instructions)

class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def size(self):
        return self.end - self.start + 1

    def __repr__(self):
        return '[' + str(self.start) + ',' + str(self.end) + ']'

rules = {}
f = open('input.txt', 'r')

workflowRegex = re.compile(r'(\w+){([^}]+)')
instructionRegex = re.compile(r'((\w+)([<>])([0-9]+):(\w+))')
for line in f:
    if line.strip() == '':
        break
    match = workflowRegex.search(line)
    name = match.group(1)
    instructions = []
    for instruction in match.group(2).split(','):
        match = instructionRegex.match(instruction)
        if match is None:
            instructions.append(Instruction(None, instruction))
        else:
            condition = Condition(match.group(2), match.group(3), int(match.group(4)))
            destination = match.group(5)
            instructions.append(Instruction(condition, destination))

    rules[name] = Rule(name, instructions)

f.close()

bfs = deque()
bfs.append(('in', []))

paths = []

while len(bfs) > 0:
    next = bfs.popleft()
    label = next[0]
    if label == 'R':
        continue
    elif label == 'A':
        paths.append(next[1])
        continue

    rule = rules[label]
    acc = []
    for instruction in rule.instructions:
        if instruction.condition is None:
            bfs.append((instruction.destination, next[1] + acc))
            break
        else:
            toAppend = acc + [instruction.condition]
            acc.append(instruction.condition.negation())
            bfs.append((instruction.destination, next[1] + toAppend))

allRangeMaps = []
total = 0
for path in paths:
    rangeMap = {
        'x': [Range(1, 4000)],
        'm': [Range(1, 4000)],
        'a': [Range(1, 4000)],
        's': [Range(1, 4000)],
    }

    for condition in path:
        condition.strip(rangeMap)
    
    total += sum(x.size() for x in rangeMap['x']) * sum(x.size() for x in rangeMap['m']) * sum(x.size() for x in rangeMap['a']) * sum(x.size() for x in rangeMap['s'])

print(total)