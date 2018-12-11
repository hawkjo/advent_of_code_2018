import re
import numpy as np
from collections import Counter, defaultdict
import time


line_re = re.compile('\[(.*)\] (.*)$')
time_re = re.compile('\d\d:(\d\d)')

recs = []
for line in open('input'):
    m = line_re.search(line)
    timestamp = m.group(1)
    rest = m.group(2)

    m = time_re.search(timestamp)
    minute = int(m.group(1))
    thetime = time.strptime(timestamp, '%Y-%m-%d %H:%M')

    recs.append((thetime, minute, rest, line))
recs.sort()


guard_re = re.compile('Guard #(\d+) begins shift')
sleep_times = defaultdict(list)
for thetime, minute, rest, line in recs:
    if rest == 'falls asleep':
        sleep_start = minute
    elif rest == 'wakes up':
        sleep_times[gid].append((sleep_start, minute))
    else:
        m = guard_re.search(rest)
        gid = int(m.group(1))
        

gids = sleep_times.keys()

totals = {gid: np.zeros((60,)) for gid in gids}
for gid, times in sleep_times.items():
    for start, end in times:
        totals[gid][start:end] += 1

big_sleeper = max(gids, key=lambda gid: totals[gid].sum())
big_minute = max(range(60), key=lambda m: totals[big_sleeper][m])

print 'Biggest sleeper'
print totals[big_sleeper]
print big_sleeper
print big_minute
print big_sleeper * big_minute


const_sleeper = max(gids, key=lambda gid: max(totals[gid]))
const_minute = max(range(60), key=lambda m: totals[const_sleeper][m])
print
print 'Most consistent sleeper'
print totals[const_sleeper]
print const_sleeper
print const_minute
print const_sleeper * const_minute
