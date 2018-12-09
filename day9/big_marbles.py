import sys
import re
from blist import *

line_re = re.compile('^(\d+) players; last marble is worth (\d+) points$')
m = line_re.search(next(open('input')))
nplayers = int(m.group(1))
last_marble_points = int(m.group(2)) * 100

a = blist([0])
pos = 0
player = 0
player_scores = [0 for _ in range(nplayers)]
for points in range(1, last_marble_points):
    if points % 1000 == 0:
        sys.stdout.write('.')
        sys.stdout.flush()
    player = (player + 1) % nplayers
    if points % 23 == 0:
        pos = (pos - 7) % len(a)
        player_scores[player] += points + a[pos]
        a = a[:pos] + a[pos+1:]
    else:
        pos = (pos + 2) % len(a)
        if pos == 0:
            a.append(points)
            pos = len(a) - 1
        else:
            a.insert(pos, points)

print
print max(player_scores)
