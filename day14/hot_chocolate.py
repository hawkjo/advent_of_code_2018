input_val = 306281
#input_val = 9

scores = [3, 7]
elf_pos = [0, 1]

while len(scores) < input_val + 10:
    total = sum(scores[pos] for pos in elf_pos)
    scores.extend([int(c) for c in str(total)])
    elf_pos = [(pos + scores[pos] + 1) % len(scores) for pos in elf_pos]

print int(''.join(map(str, scores[input_val:input_val+10])))
