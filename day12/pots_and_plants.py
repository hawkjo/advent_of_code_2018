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

        self.buff = 200
        self.pots = np.zeros((len(init_str) + 2 * self.buff), dtype=np.int)
        self.pots[self.buff:self.buff + len(init_str)] = interpret_str(init_str)

        rule_re = re.compile('([.#]{5}) => ([.#])')
        self.rules = {}
        for line in f:
            m = rule_re.search(line)
            if not m:
                continue

            self.rules[interpret_str(m.group(1))] = interpret_str(m.group(2))

    def update_pots(self):
        new_pots = np.zeros(self.pots.shape, dtype=np.int)
        for i in range(len(new_pots) - 5):
            new_pots[i+2] = self.rules[tuple([x for x in self.pots[i:i+5]])]
        self.pots = new_pots

    def idx_on_sum(self):
        return sum(i - self.buff for i, val in enumerate(self.pots) if val)


pnp = PotsAndPlants('input')
for i in range(20):
    pnp.update_pots()
print pnp.idx_on_sum()
