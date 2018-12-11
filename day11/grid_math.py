import sys
import numpy as np


input_val = 1955
#input_val = 42
M = np.zeros((301, 301))

for y in range(1, 301):
    for x in range(1, 301):
        rackid = x + 10
        cellpow = rackid * y
        cellpow += input_val
        cellpow *= rackid
        cellpow %= 1000
        cellpow = int(cellpow) / 100
        cellpow -= 5
        M[y, x] = cellpow

max_gridsum = -1000
max_x, max_y = -1, -1
for y in range(1, 301):
    for x in range(1, 301):
        gridsum = M[y:y+3, x:x+3].sum()
        if gridsum > max_gridsum:
            max_gridsum = gridsum
            max_x = x
            max_y = y

print '{},{}'.format(max_x, max_y)

max_gridsum = -1000
max_size = -1
max_x, max_y = -1, -1
for y in range(1, 301):
    if y % 3 == 0:
        sys.stdout.write('.')
        sys.stdout.flush()
    for x in range(1, 301):
        for size in range(1, 301):
            if size + x > 301 or size + y > 301:
                continue
            gridsum = M[y:y+size, x:x+size].sum()
            if gridsum > max_gridsum:
                max_gridsum = gridsum
                max_size = size
                max_x = x
                max_y = y

print
print '{},{},{}'.format(max_x, max_y, max_size)
