import sys
import re
import numpy as np
import time
from copy import deepcopy
sys.setrecursionlimit(15000)

fpath = 'input.txt'
#fpath = 'example.txt'
print_video = True

line_re = re.compile('(x|y)=(\d+), (x|y)=(\d+)\.\.(\d+)')
min_r, min_c = float('inf'), 500
max_r, max_c = 0, 0
for line in open(fpath):
    m = line_re.search(line)
    assert set([m.group(1), m.group(3)]) == set('xy'), line
    point, start, end = map(int, [m.group(i) for i in [2, 4, 5]])
    assert start < end, line
    if m.group(1) == 'x':
        min_r = min(min_r, start)
        max_r = max(max_r, end)
        min_c = min(min_c, point)
        max_c = max(max_c, point)
    else:
        min_r = min(min_r, point)
        max_r = max(max_r, point)
        min_c = min(min_c, start)
        max_c = max(max_c, end)
print 'Min/max r: {} / {}'.format(min_r, max_r)
print 'Min/max c: {} / {}'.format(min_c, max_c)

M = np.zeros((max_r+2, max_c+1), dtype=np.int)
for line in open(fpath):
    m = line_re.search(line)
    point, start, end = map(int, [m.group(i) for i in [2, 4, 5]])
    if m.group(1) == 'x':
        M[start:end+1, point] = -1
    else:
        M[point, start:end+1] = -1


# -1 = wall
# 0 = sand, not explored
# 1 = sand, flowing
# 2 = sand, filled

char_map = {
    -2: '*',
    -1: '#',
    0: '.',
    1: '|',
    2: '~',
}
def mat_str(mat):
    out_str = ''
    for row in mat:
        out_str += ''.join([char_map[i] for i in row]) + '\n'
    return out_str

def window(i, j):
    w = 20
    point = M[i, j]
    start_r, end_r = max(0, i-w), min(M.shape[0], i+w+1)
    start_c, end_c = max(0, j-w), min(M.shape[1], j+w+1)
    copy = deepcopy(M[start_r:end_r, start_c:end_c])
    copy[i - start_r, j - start_c] = -2
    return '\n' + mat_str(copy)

def print_window_and_pause(i, j, state):
    if print_video:
        print state, (i, j)
        print window(i, j)
        time.sleep(0.02)
        sys.stdout.flush()

def still(i, j, direction):
    if M[i, j] == 1:
        M[i, j] = 2
        still(i, j+direction, direction)
    else:
        assert M[i, j] == -1, window(i, j)

def flow(i, j, prev=None):
    if i > max_r or M[i, j] == 1:
        print_window_and_pause(i, j, 'flowing')
        return 'flowing'
    if M[i, j] == -1 or M[i, j] == 2:
        print_window_and_pause(i, j, 'stopped')
        return 'stopped'

    assert M[i, j] == 0, window(i, j)
    M[i, j] = 1
    state_below = flow(i+1, j, (i, j))
    if state_below == 'stopped':
        if prev == (i, j-1):
            state = flow(i, j+1, (i, j))
            print_window_and_pause(i, j, state + ' right')
            return state
        if prev == (i, j+1):
            state = flow(i, j-1, (i, j))
            print_window_and_pause(i, j, state + ' left')
            return state

        state_left = flow(i, j-1, (i, j))
        state_right = flow(i, j+1, (i, j))
        if state_left == state_right == 'stopped':
            M[i, j] = 2
            still(i, j-1, -1)
            still(i, j+1, 1)
            print_window_and_pause(i, j, 'stopped')
            return 'stopped'
    print_window_and_pause(i, j, 'flowing')
    return 'flowing'

flow(0, 500)
print
print 'Part 1:', (M[min_r:max_r+1, :] > 0).sum()
print 'Part 2:', (M == 2).sum()
