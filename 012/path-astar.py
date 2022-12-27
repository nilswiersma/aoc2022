import sys
import os
import logging
import argparse
import time

from concurrent.futures import ProcessPoolExecutor
from functools import partial
from pprint import pformat, pprint

parser = argparse.ArgumentParser()
parser.add_argument('inp', type=argparse.FileType('r'))
parser.add_argument('-v', '--verbose', action='count', default=0)
parser.add_argument('-a', '--animate', action='store_true')
args = parser.parse_args()

logging.basicConfig(format='[%(levelname)s:%(name)s:%(lineno)d] %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING - args.verbose*10)

cursor_up = lambda lines: '\x1b[{0}A'.format(lines)
cursor_down = lambda lines: '\x1b[{0}B'.format(lines)

field = None
mountains = None
end = None

class Mountain():
    def __init__(self, height, x, y):
        self.height = height
        self.x = x
        self.y = y

    def __repr__(self):
        return f'<Mountain@{id(self):x} {chr(self.height)} {self.x} {self.y}>'

def field_to_str(filter_print, filter_capitalize=None):
    ret = ''
    for xs in field:
        for c in xs:
            if filter_capitalize and filter_capitalize(c):
                ret += chr(c.height - 0x20)
            elif filter_print(c):
                ret += chr(c.height)
            else:
                ret += '.'
        ret += '\n'
    return ret

def in_field(x, y):
    return x > -1 and x < len(field[0]) and y > -1 and y < len(field)

def neighbors(m):
    return [field[y][x] for x, y in \
                filter(lambda xy: in_field(*xy), \
                       [(m.x+1, m.y), (m.x-1, m.y), (m.x, m.y+1), (m.x, m.y-1)])]

def distance_manhattan(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

def valid_move(from_, to):
    ret = from_.height + 1 == to.height or from_.height == to.height or from_.height > to.height
    return ret

def lines_to_field(ls):
    global field, mountains, end
    field = []
    mountains = []
    end = None

    for y, l in enumerate(ls):
        l = l.strip()
        field.append([])
        for x, c in enumerate(l):
            m = None
            if c == 'S':
                m = Mountain(ord('a'), x, y)
                start = m
            elif c == 'E':
                m = Mountain(ord('z'), x, y)
                end = m
            else:
                m = Mountain(ord(c), x, y)
            field[-1].append(m)
            mountains.append(m)

    return start

def path_to_str(path):
    return ''.join([chr(m.height) for m in path])

def reconstruct_path(path, m):
    ret = [m]
    while m in path.keys():
        m = path[m]
        ret.append(m)
    return ret

def astar(start):
    openset = [start]
    camefrom = {}
    gscore = {}
    fscore = {}
    for mountain in mountains:
        gscore[mountain] = sys.maxsize
        fscore[mountain] = sys.maxsize
    
    # openset.remove(start)
    gscore[start] = 0
    fscore[start] = distance_manhattan(start, end)

    shortest_l = sys.maxsize

    while openset:
        # Sort every iteration, not very smart but maybe good enough
        tmp = sorted(openset, key=lambda x: fscore[x])

        logger.debug('sorted(openset)=' + pformat(tmp))
        logger.debug('fscore=' + pformat([(x, fscore[x]) for x in openset]))
        logger.debug('gscore=' + pformat([(x, gscore[x]) for x in openset]))
        
        lowest_m = sorted(openset, key=lambda x: fscore[x])[0]
        
        if args.animate:
            path = reconstruct_path(camefrom, lowest_m)
            sys.stdout.write(field_to_str(lambda x: x in camefrom.keys(), lambda x: x in path))
            sys.stdout.write(cursor_up(len(field)))
            sys.stdout.flush()
        
        logger.debug(f'{lowest_m=}')

        if lowest_m == end:
            path = reconstruct_path(camefrom, lowest_m)
            logger.info(path_to_str(path))
            logger.info(len(path))
            shortest_l = len(path)
            break

        openset.remove(lowest_m)
        m = lowest_m

        for n in neighbors(m):
            if not valid_move(m, n):
                continue

            logger.debug(f'{n=}')

            score = gscore[m] + 1
            if score < gscore[n]:
                camefrom[n] = m
                gscore[n] = score
                fscore[n] = score + distance_manhattan(n, end)

                if n not in openset:
                    openset.append(n)
    
    if args.animate:
        sys.stdout.write(cursor_down(len(field)))
        sys.stdout.flush()

    return shortest_l

with args.inp as inp:
    ls = inp.readlines()

    # Read mountain chars to field
    start_ = lines_to_field(ls)
    logger.info('full field:\n' + field_to_str(lambda *args: True))

    answer1 = astar(start_)
    print(answer1-1)

    if args.animate:
        logger.info('turn off -a for multithreaded part')
        args.animate = False

    answer2 = sys.maxsize
    starts = list(filter(lambda x: chr(x.height) == 'a', mountains))
    
    with ProcessPoolExecutor(initializer=lines_to_field, initargs=(ls,)) as executor:
        idx = 0
        worker = partial(astar)
        for start_, tmp in zip(starts, executor.map(worker, starts)):
            idx += 1
            if tmp < answer2:
                answer2 = tmp
            logger.info(f'{idx+1=}/{len(starts)}  {start_=} {tmp=} {answer2=}')

    print(answer2-1)
