import sys
import re
from collections import defaultdict

line_re = re.compile('Step (.*) must be finished before step (.*) can begin')

graph = defaultdict(list)
for line in open('input'):
    m = line_re.search(line)
    graph[m.group(1)].append(m.group(2))

for k in graph.keys():
    graph[k] = sorted(graph[k])

def k_in_any(k):
    for v in graph.values():
        if k in v:
            return True
    return False

roots = [k for k in graph.keys() if not k_in_any(k)]
print 'Roots:', roots
print
root = min(roots)


parents = defaultdict(list)
for k, vs in graph.items():
    for v in vs:
        parents[v].append(k)


frontier = set(roots)
done = set()
while frontier:
    for k in sorted(frontier):
        if all(v in done for v in parents[k]):
            sys.stdout.write(k)
            done.add(k)
            frontier.remove(k)
            frontier.update(graph[k])
            break
