import sys
from pprint import pprint

debug = False

limit       =   100000
disk_size   = 70000000
needed_size = 30000000
counts = []

with open(sys.argv[1], 'r') as inp:
    l = inp.readline()

    dir_stack = []
    count_stack = []
    current_dir = None
    answer = 0

    while l:
        l = l.strip()
        
        if debug:
            print('\t', l)

        if l[:2] == '$ ':
            cmd, *args = l.split(' ')[1:]
            if cmd == 'cd':
                if args[0] == '..':
                    if debug:
                        print(dir_stack[-1], count_stack[-1])
                    dir_stack.pop()
                    sub_count = count_stack.pop()
                    counts.append(sub_count)
                    count_stack[-1] += sub_count
                else:
                    current_dir = args[0]
                    dir_stack.append(current_dir)
                    count_stack.append(0)
            elif cmd == 'ls':
                pass
            else:
                raise Exception(cmd, args)
        elif l[:3] == 'dir':
            pass
        else:
            file_size = int(l.split(' ')[0]) 
            count_stack[-1] += file_size

        l = inp.readline()
    
    # Fold whatever is left on the stack
    total = 0
    for _dir, sub_count in zip(dir_stack[::-1], count_stack[::-1]):
        total += sub_count
        if debug:
            print(_dir, total)
        counts.append(total)

    root_size = total
    
    print(sum(filter(lambda x: x <= limit, counts)))

    if debug:
        print(needed_size - (disk_size - root_size))

    print(min(filter(lambda x: x >= needed_size - (disk_size - root_size), counts)))
