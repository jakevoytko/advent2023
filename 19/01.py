import re

class XMAS:
    def __init__(self, x, m, a, s):
        self.x = x
        self.m = m
        self.a = a
        self.s = s
    
    def __repr__(self):
        return '{x=' + str(self.x) + ',m=' + str(self.m) + ',a=' + str(self.a) + ',s=' + str(self.s) + '}'

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

xmasregex = re.compile(r'{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}')
total = 0
for line in f:
    match = xmasregex.search(line)
    xmas = XMAS(int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4)))

    current = 'in'

    while current != 'A' and current != 'R':
        rule = rules[current]
        current = rule.execute(xmas)

    if current == 'A':
        total += xmas.x + xmas.m + xmas.a + xmas.s

print(total)

f.close()
