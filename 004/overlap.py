import sys

with open(sys.argv[1], 'r') as inp:
    l = inp.readline().strip()
    part1 = 0
    part2 = 0

    while l:
        elf0, elf1 = [[int(val) for val in elf.split('-')] for elf in l.split(',')]
        
        # full overlap
        part1 += \
            elf0[0] <= elf1[0] and elf0[1] >= elf1[1] or \
            elf0[0] >= elf1[0] and elf0[1] <= elf1[1]
        
        # partial overlap
        part2 += \
            elf0[0] >= elf1[0] and elf0[0] <= elf1[1] or \
            elf0[1] >= elf1[0] and elf0[1] <= elf1[1] or \
            elf1[1] >= elf0[0] and elf1[1] <= elf0[1] or \
            elf1[1] >= elf0[0] and elf1[1] <= elf0[1]
        
        l = inp.readline().strip()
    
    print(f'{part1=}')
    print(f'{part2=}')
