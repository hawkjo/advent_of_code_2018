import time
import numpy as np

fpath = 'input'
#fpath = 'example.txt'

stuff = '.|#'
def load_M():
    lines = [line.strip() for line in open(fpath)]
    M = np.zeros((len(lines), len(lines[0])), dtype=np.int)
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            M[i, j] = stuff.index(c)
    return M
    
def update_M(M):
    new_M = np.zeros(M.shape, dtype=np.int)
    for i in range(M.shape[0]):
        start_i = max(0, i-1)
        end_i = min(M.shape[0], i+2)
        for j in range(M.shape[1]):
            start_j = max(0, j-1)
            end_j = min(M.shape[1], j+2)
            window = M[start_i:end_i, start_j:end_j]

            if M[i, j] == 0:
                if (window == 1).sum() >= 3:
                    new_M[i, j] = 1
                else:
                    new_M[i, j] = 0
            elif M[i, j] == 1:
                if (window == 2).sum() >= 3:
                    new_M[i, j] = 2
                else:
                    new_M[i, j] = 1
            else:
                assert M[i, j] == 2, window
                if (window == 1).sum() >= 1 and (window == 2).sum() >= 2:
                    new_M[i, j] = 2
                else:
                    new_M[i, j] = 0
    return new_M

def print_M(mat):
    print
    for row in mat:
        print ''.join([stuff[i] for i in row])

M = load_M()
print_M(M)
for i in range(10):
    M = update_M(M)
    print_M(M)
    raw_input('after {} minutes'.format(i+1))

print
print 'Part 1:', (M == 1).sum() * (M == 2).sum()
print 
raw_input('Press any key for part 2...')


M = load_M()
solution_idxs = {}
for i in range(1, 100000):
    M = update_M(M)
    print i
    print_M(M)
    time.sleep(0.05)
    M_tup = tuple(M.flatten())
    if M_tup not in solution_idxs:
        solution_idxs[M_tup] = i
    else:
        sol_idx = solution_idxs[M_tup]
        period = i - sol_idx
        remainder = (1000000000 - i) % period
        solution_given_idx = {idx: sol for sol, idx in solution_idxs.items()}
        solution = np.array(solution_given_idx[sol_idx + remainder])
        break

print
print 'Part 2:', (solution == 1).sum() * (solution == 2).sum()
