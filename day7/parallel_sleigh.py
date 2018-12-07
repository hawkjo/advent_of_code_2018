import sys
import re
import time
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
root = min(roots)


parents = defaultdict(list)
for k, vs in graph.items():
    for v in vs:
        parents[v].append(k)


def time_required(c):
    return 60 + ord(c) - ord('A') + 1

frontier = set(roots)
done = []
work_times = []
i = 0
while frontier or work_times:
    ready = set(k for k in frontier if all(v in done for v in parents[k]))
    while len(work_times) < 5 and ready:
        k = min(ready)
        ready.remove(k)
        frontier.remove(k)
        work_times.append([k, time_required(k)])

    new_work_times = []
    for k, t in work_times:
        if t == 1: # had to use t == 1 so no time passes between steps
            done.append(k)
            frontier.update(graph[k])
        else:
            new_work_times.append([k, t-1])
    work_times = new_work_times

    i += 1

print
print ''.join(done)
print i
