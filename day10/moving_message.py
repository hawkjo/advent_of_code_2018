import re
import numpy as np
from copy import deepcopy
import time


class point(object):
    def __init__(self, pos, vel):
        self.init_pos = pos
        self.vel = vel
        self.curr_pos = deepcopy(pos)

    def step(self):
        self.curr_pos += self.vel

def print_points(curr_time, points):
    min_r = min(point.curr_pos[0] for point in points)
    min_c = min(point.curr_pos[1] for point in points)
    max_r = max(point.curr_pos[0] for point in points)
    max_c = max(point.curr_pos[1] for point in points)
    if max_r - min_r > 60 or max_c - min_c > 200:
        return

    M = np.zeros((max_r - min_r + 1, max_c - min_c + 1))
    for point in points:
        i = point.curr_pos[0] - min_r
        j = point.curr_pos[1] - min_c
        if 0 <= i < M.shape[0] and 0 <= j < M.shape[1]:
            M[i, j] += 1

    print
    for row in M:
        print ''.join(['#' if v else ' ' for v in row])
    print
    print (min_r, max_r), (min_c, max_c)
    print 'Current time:', curr_time
    raw_input('press key...')




points = []
line_re = re.compile('position=<\s*([-0-9]+),\s*([-0-9]+)>\s+velocity=<\s*([-0-9]+),\s*([-0-9]+)>')
for line in open('input.txt'):
    m = line_re.search(line)
    pos_c, pos_r = map(int, (m.group(1), m.group(2)))
    vel_c, vel_r = map(int, (m.group(3), m.group(4)))
    pos = np.array([pos_r, pos_c])
    vel = np.array([vel_r, vel_c])
    points.append(point(pos, vel))

curr_time = 0
while True:
    print_points(curr_time, points)
    for point in points:
        point.step()
    curr_time += 1
