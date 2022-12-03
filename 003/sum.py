import sys

def priority(c):
    priority = ord(c)   ^ 0b0100000 # flip case
    priority = priority & 0b0111111 # start from 1 instead of 0x41
    if priority > 26: return priority - 6
    return priority

def priority_sum(inp):
    l = inp.readline()
    ret = 0

    while l:
        l = l.strip()
        assert len(l) % 2 == 0

        l0 = l[:len(l)//2]
        l1 = l[len(l)//2:]
        
        unique = set(l0).intersection(l1)
        ret += sum(priority(x) for x in unique)

        l = inp.readline()
    
    print(f'part1: {ret}')

def badge_sum(inp, group_size):
    ls = [l.strip() for l in inp.readlines()]
    ret = 0
    
    for idx in range(0, len(ls), group_size):
        group = ls[idx:idx+group_size]
        badge = set(group[0]).intersection(*group[1:])
        
        assert len(badge) == 1
        
        ret = ret + priority(badge.pop())
    
    print(f'part2: {ret}')

assert priority("a") == 1
assert priority("z") == 26
assert priority("A") == 27
assert priority("Z") == 52

with open(sys.argv[1], 'r') as inp:
    priority_sum(inp)
    inp.seek(0)
    badge_sum(inp, 3)
