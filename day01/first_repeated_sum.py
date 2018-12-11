import sys

changes = [int(line.strip()) for line in open('input.txt')]
total = 0
totals = set()
while True:
    for line in open('input.txt'):
        total += int(line.strip())
        if total in totals:
            print total
            sys.exit()
        totals.add(total)
