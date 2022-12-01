import sys

def best_elves(inp, nelves):
    elves = [0]*nelves
    current = 0
    
    while True:
        l = inp.readline()
        if l == '\n' or not l:
            for elf, cal in enumerate(elves):
                if current > cal:
                    # update list and drop the last elf
                    elves = elves[:elf] + [current] + elves[elf:nelves-1]
                    break
            current = 0
            if not l:
                break
        else:
            current += int(l.strip())
    
    print(f'the best {nelves} elves carry {elves}={sum(elves)} calories')

with open(sys.argv[1], 'r') as inp:
    best_elves(inp, int(sys.argv[2]))
