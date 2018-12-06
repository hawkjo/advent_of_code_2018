import numpy as np


coords = [map(int, line.strip().split(', ')) for line in open('input')]
rs = [tup[0] for tup in coords]
cs = [tup[1] for tup in coords]

A = np.zeros((max(rs), max(cs)), dtype=np.int)

def l1(tup, ref):
    return abs(tup[0] - ref[0]) + abs(tup[1] - ref[1])

for i in range(A.shape[0]):
    for j in range(A.shape[1]):
        dists = [l1((i, j), coord) for coord in coords]
        min_dist = min(dists)
        if dists.count(min_dist) == 1:
            idx = dists.index(min_dist) + 1
            A[i, j] = idx

idxs = set(range(1, len(coords) + 1))
for i in range(A.shape[0]):
    for idx in [A[i, 0], A[i, -1]]:
        if idx in idxs: idxs.remove(idx)

for j in range(A.shape[1]):
    for idx in [A[0, j], A[-1, j]]:
        if idx in idxs: idxs.remove(idx)

print max((A == idx).sum() for idx in idxs)


B = np.zeros((max(rs), max(cs)), dtype=np.int)

for i in range(B.shape[0]):
    for j in range(B.shape[1]):
        total = sum(l1((i, j), coord) for coord in coords)
        if total < 10000:
            B[i, j] = 1
            if i == 0 or j == 0 or i == B.shape[0] - 1 or j == B.shape[1] - 1:
                print 'Yikes!!'

print (B == 1).sum()

