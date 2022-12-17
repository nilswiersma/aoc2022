import sys
import numpy as np

debug = False

def adjacent(H, T):
    if H == T:
        return True

    dx = abs(H[0] - T[0])
    dy = abs(H[0] - T[0])
    return dy <= 1 and dx <= 1

def trace_to_grid(trace):
    grid = np.empty((5,5), dtype=str)
    grid.fill('.')
    for t in trace:
        grid[t[0]][t[1]] = '#'
    return grid

with open(sys.argv[1], 'r') as inp:
    l = inp.readline().strip()
    
    H = [0,0]
    T = [0,0]

    T_trace = [tuple(T)]

    if debug:
        print(f'{H=}')
        print(f'{T=}')

    while l:
        d, c = l.split(' ')
        c = int(c)
        
        # Move H
        if d == 'U':
            H[1] += c
        elif d == 'D':
            H[1] -= c
        elif d == 'R':
            H[0] += c
        elif d == 'L':
            H[0] -= c
        
        if debug:
            print(f'[+] {l=}')
            print(f'{H=}')
        
        # Move T
        while True:
            d = H[0] - T[0], H[1] - T[1]
            
            if debug:
                print(f'{d=}')
            
            if abs(d[0]) <= 1 and abs(d[1]) <= 1:
                break
            
            # The first step is always diagonal, so include the +1/-1
            # in the first step as well
            if abs(d[0]) == 1 and abs(d[1]) > 1:
                T[0] += d[0]
                dim = 1
            elif abs(d[1]) == 1 and abs(d[0]) > 1:
                T[1] += d[1]
                dim = 0
            else: 
                if abs(d[0]) > abs(d[1]):
                    dim = 0
                else:
                    dim = 1
            step = -1 if d[dim] < 0 else 1
            T[dim] += step
            T_trace.append(tuple(T))
            
            if debug:
                print(f'{T=}')
                print(f'{T_trace=}')
        l = inp.readline().strip()
    
    if debug:
        print(np.rot90(trace_to_grid(T_trace), k=1))     
    
    print(len(set(T_trace)))
