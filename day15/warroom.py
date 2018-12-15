import sys
import numpy as np
from copy import deepcopy


class WarRoom(object):
    movements = [
        np.array([-1,  0]),
        np.array([ 1,  0]),
        np.array([ 0, -1]),
        np.array([ 0,  1]),
    ]

    def __init__(self, fpath):
        self.rounds = 0
        self.warriors = []
        self.room_map = []
        for r, line in enumerate(open(fpath)):
            room_line = []
            for c, char in enumerate(line):
                if char in 'EG':
                    self.warriors.append(Warrior(r, c, char, self))
                    room_line.append('.')
                elif char == '\n':
                    pass
                else:
                    assert char in '.#', (char, line)
                    room_line.append(char)
            self.room_map.append(room_line)
        self.room_shape = (len(self.room_map), len(self.room_map[0]))

    def still_fighting(self):
        return len(set(w.race for w in self.warriors)) == 2

    def take_round(self):
        for w in self.warriors:
            w.had_turn = False

        while True:
            self.warriors.sort(key=lambda w: w.pos)
            for w in self.warriors:
                if not w.had_turn:
                    if not self.still_fighting():
                        return
                    w.take_turn()
                    break
            else:
                self.rounds += 1
                break

            self.warriors = [w for w in self.warriors if w.hit_points > 0]

    def is_open(self, pos):
        if (min(pos) < 0
                or pos[0] >= self.room_shape[0]
                or pos[1] >= self.room_shape[1]):
            return False

        if self.room_map[pos[0]][pos[1]] == '#':
            return False

        for warrior in self.warriors:
            if pos == warrior.pos:
                return False

        return True

    def __str__(self):
        room_map = deepcopy(self.room_map)
        for warrior in self.warriors:
            room_map[warrior.pos[0]][warrior.pos[1]] = warrior.race
        out_str = ''
        for i, room_line in enumerate(room_map):
            out_str += ''.join(room_line)
            out_str += '   '
            out_str += ', '.join(['{}({})'.format(w.race, w.hit_points)
                                  for w in self.warriors if w.pos[0] == i])
            out_str += '\n'
        return out_str

    def adjacents(self, pos):
        adj_spaces = []
        for m in self.movements:
            adj = np.array(pos) + m
            adj_spaces.append((adj[0], adj[1]))
        return adj_spaces

    def open_adjacents(self, pos):
        return [adj for adj in self.adjacents(pos) if self.is_open(adj)]


class Warrior(object):
    def __init__(self, r, c, race, warroom):
        self.pos = (r, c)
        self.race = race
        self.warroom = warroom
        self.hit_points = 200
        self.attack_power = 3
        self.had_turn = False

    def __str__(self):
        return '{}{}'.format(self.race, self.pos)

    @property
    def enemies_in_range(self):
        return [w for w in self.warroom.warriors if w.race != self.race
                and w.pos in self.warroom.adjacents(self.pos)]

    def take_turn(self):
        if not self.enemies_in_range:
            self.move()
        if self.enemies_in_range:
            enemy = min(self.enemies_in_range, key=lambda w: (w.hit_points, w.pos[0], w.pos[1]))
            enemy.take_damage(self.attack_power)
        self.had_turn = True

    def take_damage(self, damage):
        self.hit_points -= damage

    def move(self):
        enemies = [w for w in self.warroom.warriors if w.race != self.race]
        pos_in_range = set([pos for enemy in enemies
                            for pos in enemy.open_adjacents()])

        frontier = {pos: 1 for pos in self.open_adjacents()}
        closed = {self.pos: 0}

        min_score = float('inf')
        curr_score = float('inf')
        while frontier and (min_score == float('inf') or curr_score == min_score):
            curr_node = min(frontier.items(), key=lambda tup: tup[1])
            curr_pos, curr_score = curr_node
            for adj_pos in self.warroom.open_adjacents(curr_pos):
                if not (adj_pos in closed or adj_pos in frontier):
                    frontier[adj_pos] = curr_score + 1
            del frontier[curr_pos]
            closed[curr_pos] = curr_score

            if curr_pos in pos_in_range:
                min_score = min(min_score, curr_score)

        if min_score == float('inf'): # nowhere to go
            return

        def all_adj_on_path(pos):
            for adj in self.warroom.adjacents(pos):
                if adj in closed:
                    if closed[adj] == 0:
                        yield pos
                    elif closed[adj] == closed[pos] - 1:
                        for new_adj in all_adj_on_path(adj):
                            yield new_adj

        end_pos = min(pos for pos in pos_in_range if pos in closed and closed[pos] == min_score)
        all_adj = all_adj_on_path(end_pos)

        if all_adj:
            self.pos = min(all_adj)

    def open_adjacents(self):
        return self.warroom.open_adjacents(self.pos)




fpath = 'input.txt'
#fpath = 'example6.txt'
verbose = False

wr = WarRoom(fpath)
print wr
raw_input('Press key to continue...')
while wr.still_fighting():
    wr.take_round()
    if verbose:
        print 'After {} rounds:'.format(wr.rounds)
        print wr
        raw_input('Press key to continue...')
print wr
print 'Rounds:', wr.rounds
print 'Sum hit points:', sum(w.hit_points for w in wr.warriors)
print 'Product:', wr.rounds * sum(w.hit_points for w in wr.warriors)
