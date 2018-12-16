from copy import deepcopy

def addr(reg, a, b, c):
    reg[c] = reg[a] + reg[b]
    return reg

def addi(reg, a, b, c):
    reg[c] = reg[a] + b
    return reg

def mulr(reg, a, b, c):
    reg[c] = reg[a] * reg[b]
    return reg

def muli(reg, a, b, c):
    reg[c] = reg[a] * b
    return reg

def banr(reg, a, b, c):
    reg[c] = reg[a] & reg[b]
    return reg

def bani(reg, a, b, c):
    reg[c] = reg[a] & b
    return reg

def borr(reg, a, b, c):
    reg[c] = reg[a] | reg[b]
    return reg

def bori(reg, a, b, c):
    reg[c] = reg[a] | b
    return reg

def setr(reg, a, b, c):
    reg[c] = reg[a]
    return reg

def seti(reg, a, b, c):
    reg[c] = a
    return reg

def gtir(reg, a, b, c):
    reg[c] = int(a > reg[b])
    return reg

def gtri(reg, a, b, c):
    reg[c] = int(reg[a] > b)
    return reg

def gtrr(reg, a, b, c):
    reg[c] = int(reg[a] > reg[b])
    return reg

def eqir(reg, a, b, c):
    reg[c] = int(a == reg[b])
    return reg

def eqri(reg, a, b, c):
    reg[c] = int(reg[a] == b)
    return reg

def eqrr(reg, a, b, c):
    reg[c] = int(reg[a] == reg[b])
    return reg

funcs = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]
assert len(funcs) == 16

breg = [3, 2, 1, 1]
inst = [9, 2, 1, 2]
areg = [3, 2, 2, 1]
print 'Example possibilities:'
for f in funcs:
    if f(deepcopy(breg), *inst[1:]) == areg:
        print f.__name__

tests = []
prog = []
with open('input.txt') as f:
    line = next(f)
    while line:
        if line.startswith('Before:'):
            breg = eval(line.strip()[8:])
            line = next(f)
            inst = map(int, line.strip().split())
            line = next(f)
            areg = eval(line.strip()[8:])
            line = next(f)
            tests.append((breg, inst, areg))
        elif line.strip() == '':
            line = next(f)
        else:
            inst = map(int, line.strip().split())
            prog.append(inst)
            try:
                line = next(f)
            except StopIteration:
                break

print
print 'Tests:', len(tests)
print 'Prog lines:', len(prog)

num_with_three = 0
for breg, inst, areg in tests:
    if sum(1 for f in funcs if f(deepcopy(breg), *inst[1:]) == areg) >= 3:
        num_with_three += 1
print
print 'Tests with >= 3:', num_with_three



func_nums = {f: set(range(16)) for f in funcs}
for breg, inst, areg in tests:
    for f in funcs:
        if inst[0] in func_nums[f] and f(deepcopy(breg), *inst[1:]) != areg:
            func_nums[f].remove(inst[0])

while max(len(v) for v in func_nums.values()) > 1:
    for f in funcs:
        if len(func_nums[f]) == 1:
            n = list(func_nums[f])[0]
            for otherf in funcs:
                if f != otherf and n in func_nums[otherf]:
                    func_nums[otherf].remove(n)

func_given_num = {list(v)[0]: f for f, v in func_nums.items()}
print
for i in range(16):
    print i, func_given_num[i].__name__

reg = [0, 0, 0, 0]
for inst in prog:
    func_given_num[inst[0]](reg, *inst[1:])
print
print 'Program output:'
print reg
