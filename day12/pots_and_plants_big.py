import re
import numpy as np


def interpret_str(s):
    a = []
    for c in s:
        if c == '.':
            a.append(0)
        else:
            assert c == '#', s
            a.append(1)

    if len(a) == 1:
        return a[0]
    else:
        return tuple(a)


class PotsAndPlants(object):
    def __init__(self, fpath):
        f = open(fpath)
        init_line = next(f).strip()
        start = min(init_line.index('.'), init_line.index('#'))
        init_str = init_line[start:]

        self.buff = 150
        self.pots = np.zeros((len(init_str) + 2 * self.buff), dtype=np.int)
        self.pots[self.buff:self.buff + len(init_str)] = interpret_str(init_str)

        rule_re = re.compile('([.#]{5}) => ([.#])')
        self.rules = {}
        for line in f:
            m = rule_re.search(line)
            if not m:
                continue

            self.rules[interpret_str(m.group(1))] = interpret_str(m.group(2))

        self.generation = 0
        self.first_shift_gen = None
        self.first_shift_pots = None

    def update_pots(self):
        self.generation += 1
        new_pots = np.zeros(self.pots.shape, dtype=np.int)
        for i in range(len(new_pots) - 5):
            new_pots[i+2] = self.rules[tuple([x for x in self.pots[i:i+5]])]
        if not self.first_shift_gen and (new_pots[1:] == self.pots[:-1]).all():
            self.first_shift_gen = self.generation
            self.first_shift_pots = new_pots
        self.pots = new_pots

    def idx_on_sum(self):
        return sum(i - self.buff for i, val in enumerate(self.pots) if val)

    def __str__(self):
        return ''.join(['#' if xx else '.' for xx in self.pots[self.buff:]])

    def get_big_idx_on_sum(self, n):
        while self.first_shift_gen is None:
            self.update_pots()
        return sum(i - self.buff + (n - self.first_shift_gen)
                   for i, val in enumerate(self.first_shift_pots) if val)


pnp = PotsAndPlants('input')
print pnp
for i in range(120):
    pnp.update_pots()
    print pnp

print 
print pnp.get_big_idx_on_sum(50000000000)
