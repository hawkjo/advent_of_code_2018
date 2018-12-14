input_val = 306281
#input_val = 51589      # 9
#input_val = 92510      # 18
#input_val = 59414      # 2018
input_val_len = len(str(input_val))

scores = [3, 7]
elf_pos = [0, 1]

def get_last_ints(scores):
    return int(''.join(map(str, scores[-input_val_len:]))), int(''.join(map(str, scores[-input_val_len-1:-1])))

while input_val not in get_last_ints(scores):
    total = sum(scores[pos] for pos in elf_pos)
    scores.extend([int(c) for c in str(total)])
    elf_pos = [(pos + scores[pos] + 1) % len(scores) for pos in elf_pos]

print len(scores) - input_val_len - get_last_ints(scores).index(input_val)
