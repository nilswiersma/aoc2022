import sys
from enum import Enum, auto

debug_clock = False
debug_scanline = False
debug_CRT = False

class State(Enum):
    START = auto()
    STOP = auto()
    NOOP = auto()
    ADDX1 = auto()
    ADDX2 = auto()

LIGHT = '█'
DARK = ' '

state = State.START
X = 1
CRT = None
scanline = [LIGHT]*3 + [DARK]*37

def move_sprite():
    global scanline
    scanline = [DARK]*40
    for idx in range(X-1, X+2):
        scanline[idx%40] = LIGHT
    if debug_scanline:
        print(''.join(scanline))

def draw_pixel(cycle):
    ypos = (cycle//40) % 6
    xpos = cycle % 40
    CRT[ypos][xpos] = scanline[xpos]
    if debug_CRT:
        print(f'@{cycle+1:03d} {ypos,xpos} {X=} {scanline[xpos]=}')
        print(''.join(scanline))
        print(''.join(CRT[ypos]))

def print_CRT():
    print('='*40)
    for line in CRT:
        print(''.join(line))
    print('='*40)

def clear_CRT():
    global CRT
    CRT = [['']*40 for _ in range(6)] 

def read_ins(inp):
    l = inp.readline().strip()
    return l.split(' ')

def parse_ins(ins, *args):
    if ins == 'noop':
        state = State.NOOP
    elif ins == 'addx':
        state = State.ADDX1
    else:
        state = State.STOP
    return state

with open(sys.argv[1], 'r') as inp:
    ret1 = 0
    clear_CRT()

    for cycle in range(0,9999):
        if cycle % 40 == 20:
            ret1 += cycle * X
        if debug_clock:
            print(f'@{cycle:03d} {X=}', end=' ')   

        if cycle > 0 and cycle % 240 == 0:
            print_CRT()
            clear_CRT()
        
        if state != State.START:
            draw_pixel(cycle-1) # cycle starts a 1, CRT at 0

        if state == State.STOP:
            if debug_clock:
                print()
            break
        elif state == State.START or state == State.NOOP:
            ins, *args = read_ins(inp)
            state = parse_ins(ins, args)
        elif state == State.ADDX1:
            state = State.ADDX2
        elif state == State.ADDX2:
            X += int(args[0])
            move_sprite()
            ins, *args = read_ins(inp)
            state = parse_ins(ins, args)
        
        if debug_clock:
            print(f'-> {X=}')
    
    print(ret1)
    print('RJERPEFC')
