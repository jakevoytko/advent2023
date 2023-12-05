from functools import reduce

f = open('input.txt', 'r')

class Span:
    def __init__(self, start, end):
        if end <= start:
            raise Exception('Invalid span')
        self.start = start
        self.end = end
    
    def intersects(self, other):
        return self.start >= other.start and self.start < other.end or other.start >= self.start and other.start < self.end

    def intersection(self, other):
        if not self.intersects(other):
            return None
        return Span(max(self.start, other.start), min(self.end, other.end))

    def subtract(self, other):
        if not self.intersects(other):
            return [self]
        if self.start >= other.start:
            if self.end <= other.end:
                return []
            return [Span(other.end, self.end)]

        if self.end <= other.end:
            if self.start >= other.start:
                return []
            return [Span(self.start, other.start)]
        
        return [Span(self.start, other.start), Span(other.end, self.end)]
    
    def __repr__(self):
        return f'[{self.start}, {self.end})'

seedLine = f.readline()
seeds = [int(c) for c in seedLine.split(' ')[1:] if c != '']

seedRanges = set()
for i in range(0, len(seeds), 2):
    seedRanges.add(Span(seeds[i], seeds[i] + seeds[i+1]))

f.readline()

expectingNewConversion = True

def splice(seedRanges, sourceRange, destStart):
    mappedRanges = set()
    remainingRanges = set()

    for seedRange in seedRanges:
        if not seedRange.intersects(sourceRange):
            remainingRanges.add(seedRange)
            continue
        intersection = seedRange.intersection(sourceRange)
        remaining = seedRange.subtract(sourceRange)
        mappedRanges.add(Span(destStart + intersection.start - sourceStart, destStart + intersection.end - sourceStart))
        remainingRanges.update(set(remaining))

    return remainingRanges, mappedRanges

newSeedRanges = set()
for line in f:
    if expectingNewConversion:
        expectingNewConversion = False
        continue
    
    if line == '\n':
        expectingNewConversion = True
        newSeedRanges.update(seedRanges)
        seedRanges = newSeedRanges
        newSeedRanges = set()
        continue

    destStart, sourceStart, num = [int(x) for x in line.strip().split(' ') if x != '']
    sourceRange = Span(sourceStart, sourceStart + num)
    seedRanges, mappedRanges = splice(seedRanges, sourceRange, destStart)
    newSeedRanges.update(mappedRanges)

newSeedRanges.update(seedRanges)
seedRanges = newSeedRanges

print(reduce(lambda a, b: min(a, b.start), seedRanges, 2**256))

f.close()
