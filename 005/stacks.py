import sys
import re

ins_re = r'move (\d+) from (\d+) to (\d+)'

def read_stacks(inp):
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
    
    return stacks

def process_file(inp, process_instruction):
    stacks = read_stacks(inp)
    
    l = inp.readline()
    while l:
        m = re.match(ins_re, l)
        assert len(m.groups()) == 3
        process_instruction(stacks, *[int(x) for x in m.groups()])

        l = inp.readline()

    print(''.join([stack.pop().replace('[', '').replace(']', '') for stack in stacks]))

def part1(stacks, mov_count, mov_from, mov_to):
    for _ in range(mov_count):
        crate = stacks[mov_from-1].pop()
        stacks[mov_to-1].append(crate)

def part2(stacks, mov_count, mov_from, mov_to):
    crates = stacks[mov_from-1][-1*mov_count:]
    stacks[mov_from-1] = stacks[mov_from-1][:-1*mov_count]
    stacks[mov_to-1] += crates

with open(sys.argv[1], 'r') as inp:
    print('part1',)
    process_file(inp, part1)
    inp.seek(0)
    print('part2',)
    process_file(inp, part2)
 
