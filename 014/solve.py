import sys
import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('inp', type=argparse.FileType('r'))
parser.add_argument('answer', help='solve 1 or 2', nargs=1, choices=('1', '2'))
parser.add_argument('-v', '--verbose', action='count', default=0)
args = parser.parse_args()

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.WARNING - args.verbose*10)

coords = []
range_x = [500, 500]
range_y = [0,0]

coords.append([(500, 0, '+')])

with args.inp as inp:
    l = inp.readline()
    while l:
        l = l.strip()
        logger.debug(l)

        l = l.split(' -> ')
        coords.append([])
        for coord in l:
            x, y = map(int, coord.split(','))
            logger.debug(f'{x}, {y}')
            coords[-1].append((x, y, '#'))

            if x < range_x[0]:
                range_x[0] = x
            if x > range_x[1]:
                range_x[1] = x
            if y < range_y[0]:
                range_y[0] = y
            if y > range_y[1]:
                range_y[1] = y

            logger.debug(f'{range_x=} {range_y=}')
        l = inp.readline()

    logger.info(f'{range_x=} {range_y=}')

range_x[1] += 1
range_y[1] += 1

logger.info(f'{range_x=} {range_y=}')

wall = [['.']*(range_x[1] - range_x[0]) for _ in range(range_y[1]-range_y[0])]
logger.info(f'{len(wall)=} {len(wall[0])=}')

def print_wall():
    ret = ['    ' + ''.join(f'{(range_x[0]+x)%10:d}' for x in range(range_x[1]-range_x[0]))]
    for y, l in enumerate(wall):
        ret.append(f'{range_y[0]+y:3d} ' + ''.join(l))
    return '\n'.join(ret)

for l in coords:
    x, y, mark = l[0]
    x_start = x
    y_start = y
    logger.debug('')
    wall[y_start-range_y[0]][x_start-range_x[0]] = mark
    for x_end, y_end, mark in l[1:]:
        logger.debug(f'{x_start=} {y_start=}')
        if x_start == x_end and y_start < y_end:
            it = zip([x_start]*(y_end-y_start), range(y_start, y_end))
        elif x_start == x_end and y_start > y_end:
            it = zip([x_start]*(y_start-y_end), range(y_start, y_end, -1))
        elif y_start == y_end and x_start < x_end:
            it = zip(range(x_start, x_end), [y_start]*(x_end-x_start))
        elif y_start == y_end and x_start > x_end:
            it = zip(range(x_start, x_end, -1), [y_start]*(x_start-x_end))
        
        for x, y in it:
            logger.debug(f'-> {x=}, {y=} {x-range_x[0]=} {y-range_y[0]=}')
            wall[y-range_y[0]][x-range_x[0]] = mark
        wall[y_end-range_y[0]][x_end-range_x[0]] = mark
        
        logger.debug(f'{x_end=} {y_end=}')

        x_start = x_end
        y_start = y_end

logger.info('\n' + print_wall())

if args.answer[0] == '1':
    queue = [(500, 0)]
    sand = 0

    try:
        while queue:
            coord = queue.pop(0)
            
            x = coord[0] - range_x[0]
            y = coord[1] - range_y[0]
            mark = wall[y+1][x]
            if mark == '.':
                queue.append((coord[0], coord[1]+1))
            elif mark == '#' or mark == 'o':
                mark = wall[y+1][x-1]
                if mark == '.':
                    queue.append((coord[0]-1, coord[1]+1))
                elif mark == '#' or mark == 'o':
                    mark = wall[y+1][x+1]
                    if mark == '.':
                        queue.append((coord[0]+1, coord[1]+1))
                    elif mark == '#' or mark == 'o':
                        wall[y][x] = 'o'
                        sand += 1
                        queue.append((500, 0))
    except IndexError:
        logger.info('\n' + print_wall())
        print(sand)
elif args.answer == ['2']:
    queue = [(500, 0)]
    sand = 0
    
    wall.append(['.']*(range_x[1]-range_x[0]))
    wall.append(['#']*(range_x[1]-range_x[0]))
    range_y[1] = range_y[1] + 2

    logger.info('\n' + print_wall())
    
    try:
        while queue:
            coord = queue.pop(0)
            logger.debug(f'{coord=} {range_x=} {range_y=}')
            if coord[0]-1 < range_x[0]:
                for idx in range(len(wall)):
                    wall[idx] = ['.' if idx+1 != range_y[1] else '#'] + wall[idx]
                range_x[0] = range_x[0]-1
                assert range_x[0] == coord[0]-1
            elif coord[0]+1 > range_x[1]-1:
                for idx in range(len(wall)):
                    wall[idx] = wall[idx] + ['.' if idx+1 != range_y[1] else '#']
                range_x[1] = range_x[1]+1
                assert range_x[1]-1 == coord[0]+1

            x = coord[0] - range_x[0]
            y = coord[1] - range_y[0]

            mark = wall[y+1][x]
            logger.debug(f'{mark=}')
            if coord == (500, 0) and wall[y][x] == 'o':
                raise IndexError
            elif mark == '.':
                queue.append((coord[0], coord[1]+1))
            elif mark == '#' or mark == 'o':
                mark = wall[y+1][x-1]
                if mark == '.':
                    queue.append((coord[0]-1, coord[1]+1))
                elif mark == '#' or mark == 'o':
                    mark = wall[y+1][x+1]
                    if mark == '.':
                        queue.append((coord[0]+1, coord[1]+1))
                    elif mark == '#' or mark == 'o':
                        wall[y][x] = 'o'
                        sand += 1
                        queue.append((500, 0))
    except IndexError:
        logger.info('\n' + print_wall())
        print(sand)
