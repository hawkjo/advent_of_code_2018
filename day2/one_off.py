def simple_ham(s1, s2):
    return sum(1 for c1, c2 in zip(s1, s2) if c1 != c2)

ids = [line.strip() for line in open('input.txt')]

for i, id1 in enumerate(ids):
    for id2 in ids[i+1:]:
        if simple_ham(id1, id2) == 1:
            print ''.join(c1 for c1, c2 in zip(id1, id2) if c1 == c2)
