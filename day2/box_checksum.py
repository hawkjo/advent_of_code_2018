from collections import Counter
twos, threes = 0, 0
for line in open('input.txt'):
    cntr = Counter(line.strip())
    if 2 in cntr.values():
        twos += 1
    if 3 in cntr.values():
        threes += 1
print twos * threes
