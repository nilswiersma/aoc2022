import sys
import numpy as np

debug = False
rope_len = int(sys.argv[2])

def adjacent(H, T):
    if H == T:
        return True

    dx = abs(H[0] - T[0])
    dy = abs(H[0] - T[0])
    return dy <= 1 and dx <= 1

def trace_to_grid(trace):
    grid = np.empty((20,20), dtype=str)
    grid.fill('.')
    for d, t in enumerate(trace):
        grid[t[0]%20][t[1]%20] = f'{d:x}'
    return grid

with open(sys.argv[1], 'r') as inp:
    l = inp.readline().strip()
    
    rope = [ [0,0] for _ in range(rope_len+1) ]

    T_trace = [tuple(rope[-1])]

    if debug:
        print(f'{rope[0]=}')
        print(f'{rope[-1]=}')

    while l:
        d, c = l.split(' ')
        
        c = int(c)
        
        # Direction for H
        if d == 'U':
            xy = 1
            sign = 1
        elif d == 'D':
            xy = 1
            sign = -1
        elif d == 'R':
            xy = 0
            sign = 1
        elif d == 'L':
            xy = 0
            sign = -1
        
        if debug:
            print(f'[+] {l=}')
        
        for _ in range(c): 
            # Move rope
            for rope_idx in range(len(rope)):
                # Move head
                if rope_idx == 0:
                    rope[rope_idx][xy] += sign
                
                # Move the rest based on the previous rope_idx
                else:
                    d = [rope[rope_idx-1][0] - rope[rope_idx][0], rope[rope_idx-1][1] - rope[rope_idx][1]]
                    d_abs = [abs(x) for x in d]
                    step = [0, 0]
                    if 2 not in d_abs:
                        # rope_idx is touching rope_idx-1 (also diagonally)
                        # Can also skip the other knots
                        if debug:
                            print('touching')
                        break
                    else:
                        step = d
                        if d_abs[0] == 2:
                            step[0] = step[0] >> 1
                        if d_abs[1] == 2:
                            step[1] = step[1] >> 1
                    rope[rope_idx][0] += step[0]
                    rope[rope_idx][1] += step[1]
                    
                    if rope_idx == rope_len:
                        T_trace.append(tuple(rope[rope_idx]))
     
        if debug:
            print(f'{rope=}')
            with np.printoptions(threshold=10000, linewidth=200):
                print(np.rot90(trace_to_grid(rope), k=1)) 
                input(f'{l=} next frame?')
    
        l = inp.readline().strip()
    
    if debug:
        with np.printoptions(threshold=10000, linewidth=200):
            print(np.rot90(trace_to_grid(T_trace), k=1))     
    
    print(len(set(T_trace)))
