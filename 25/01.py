from collections import defaultdict, deque
import graphviz

f = open('input.txt', 'r')

connections = defaultdict(set)
plugs = []

graph = graphviz.Graph()
for line in f:
  source, dest = line.strip().split(':')
  for i in dest.strip().split(' '):
    connections[source].add(i)
    connections[i].add(source)
    plugs.append((source, i))
    graph.edge(source, i)

f.close()

#graph.render('graph.gv', view=True, engine='neato')

def connected(connections):
  visited = set()
  groups = []
  for node in connections:
    if node not in visited:
      q = deque([node])
      grouplen = 0
      while q:
        n = q.popleft()
        if n not in visited:
          visited.add(n)
          grouplen += 1
          q.extend(connections[n])
      groups.append(grouplen)
  return groups

connections['qqq'].remove('mlp')
connections['mlp'].remove('qqq')
connections['qdp'].remove('jxx')
connections['jxx'].remove('qdp')
connections['zbr'].remove('vsx')
connections['vsx'].remove('zbr')

result = connected(connections)
print(result[0] * result[1])