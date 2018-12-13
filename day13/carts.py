import sys
import numpy as np
from copy import deepcopy


class Cart(object):
    turn_left = np.array([
        [0, -1],
        [1,  0]
    ])
    turn_right = np.array([
        [ 0, 1],
        [-1, 0]
    ])
    go_straight = np.array([
        [1, 0],
        [0, 1]
    ])
    intersection_actions = [turn_left, go_straight, turn_right]

    def __init__(self, r, c, vel):
        self.pos = np.array([r, c])
        self.vel = vel
        self.intersection_idx = 0

    def add_tracks(self, tracks):
        self.tracks = tracks

    def update_vel(self):
        track_char = self.tracks[self.pos[0]][self.pos[1]] 

        if track_char == '\\':
            self.vel = np.array([self.vel[1], self.vel[0]])
        elif track_char == '/':
            self.vel = -np.array([self.vel[1], self.vel[0]])
        elif track_char == '+':
            self.vel = np.dot(self.intersection_actions[self.intersection_idx], self.vel)
            self.intersection_idx = (self.intersection_idx + 1) % 3
        else:
            assert track_char in '-|', track_char

    def step(self):
        self.pos += self.vel
        self.update_vel()

    @property
    def pos_tuple(self):
        return (self.pos[0], self.pos[1])

    def collides_with(self, other_cart):
        return all(self.pos == other_cart.pos)


fpath = 'input.txt'
#fpath = 'example.txt'
#fpath = 'example_nocollision.txt'

carts = []
track_map = []
for r, line in enumerate(open(fpath)):
    track_line = []
    for c, char in enumerate(line):
        if char == '>':
            carts.append(Cart(r, c, np.array([0, 1])))
            track_line.append('-')
        elif char == '<':
            carts.append(Cart(r, c, np.array([0, -1])))
            track_line.append('-')
        elif char == '^':
            carts.append(Cart(r, c, np.array([-1, 0])))
            track_line.append('|')
        elif char == 'v':
            carts.append(Cart(r, c, np.array([1, 0])))
            track_line.append('|')
        elif char == '\n':
            pass
        else:
            track_line.append(char)
    track_map.append(track_line)

for cart in carts:
    cart.add_tracks(track_map)

def print_map(track_map, carts):
    track_map = deepcopy(track_map)
    for cart in carts:
        track_map[cart.pos[0]][cart.pos[1]] = '*'
    for track_line in track_map:
        print ''.join(track_line)

if False:
    # Part 1
    while True:
        carts.sort(key=lambda cart: cart.pos_tuple)
        #print_map(track_map, carts)
        for i, cart in enumerate(carts):
            cart.step()
            if any(cart.collides_with(other_cart) for other_cart in carts[:i] + carts[i+1:]):
                print_map(track_map, carts)
                print '{},{}'.format(cart.pos[1], cart.pos[0])
                sys.exit()

else:
    # Part 2
    while True:
        assert len(carts) > 0

        if len(carts) == 1:
            print_map(track_map, carts)
            cart = carts[0]
            print '{},{}'.format(cart.pos[1], cart.pos[0])
            break
    
        carts.sort(key=lambda cart: cart.pos_tuple)
        #print_map(track_map, carts)
        i = 0
        while i < len(carts):
            cart = carts[i]
            cart.step()
            for j in range(len(carts)):
                if i != j and cart.collides_with(carts[j]):
                    first, second = min(i, j), max(i, j)
                    assert first < second
                    carts = carts[:first] + carts[first+1:second] + carts[second+1:]
                    if i == second:
                        i -= 1 
                    # if i == first, stay in same spot
                    break
            else:
                i += 1
