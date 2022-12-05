import sys
import re

with open(sys.argv[1], 'r') as inp:
    stacks_s = []

    l = inp.readline()
    while l != '\n':
        stacks_s.append(l[:-1])
        l = inp.readline()

    stack_count = len(stacks_s[-1].split('   '))
    stacks = [[] for _ in range(stack_count)]
   
    for l in stacks_s[:-1]:
        for idx in range(0, stack_count):
            crate = l[idx*4:idx*4+4].strip()
            if crate:
                stacks[idx].append(crate)
    
    stacks = [stack[::-1] for stack in stacks]

    ins_re = r'move (\d+) from (\d+) to (\d+)'
    
    l = inp.readline()
    while l:
        m = re.match(ins_re, l)
        mov_count, mov_from, mov_to = m.groups()

        for _ in range(int(mov_count)):
            crate = stacks[int(mov_from)-1].pop()
            stacks[int(mov_to)-1].append(crate)

        l = inp.readline()

    print(''.join([stack.pop().replace('[', '').replace(']', '') for stack in stacks]))
