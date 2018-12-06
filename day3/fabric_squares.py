import re
import numpy as np

A = np.zeros((1000, 1000), dtype=np.int8)

line_re = re.compile('#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')
for line in open('input'):
    m = line_re.match(line)
    user = int(m.group(1))
    x = int(m.group(2))
    y = int(m.group(3))
    w = int(m.group(4))
    h = int(m.group(5))
    A[x:x+w, y:y+h] += 1

print (A > 1).sum()

for line in open('input'):
    m = line_re.match(line)
    user = int(m.group(1))
    x = int(m.group(2))
    y = int(m.group(3))
    w = int(m.group(4))
    h = int(m.group(5))
    if (A[x:x+w, y:y+h] == 1).all():
        print user
