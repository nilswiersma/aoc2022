import sys
import os
import logging
import argparse
import re
import itertools

import z3

from concurrent.futures import ProcessPoolExecutor
from functools import partial
from pprint import pformat, pprint

parser = argparse.ArgumentParser()
parser.add_argument('inp', type=argparse.FileType('r'))
parser.add_argument('-y', help='y line for answer1', type=int)
parser.add_argument('-m', help='x and y bounds for answer2', type=int)
parser.add_argument('-v', '--verbose', action='count', default=0)
args = parser.parse_args()

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.WARNING - args.verbose*10)

regex = r"Sensor at x=(-?\d*), y=(-?\d*): closest beacon is at x=(-?\d*), y=(-?\d*)"

def distance_manhattan(ax, ay, bx, by):
    return abs(ax - bx) + abs(ay - by)

def read_sensors(ls):
    global sensors
    global test

    test = [1,2,3]
    test = {1: 2, 3: 4}

    sensors = {}

    for match in re.finditer(regex, ls, re.MULTILINE):
        sensor = int(match.group(1)), int(match.group(2))
        beacon = int(match.group(3)), int(match.group(4))
        assert sensor not in sensors.keys()
        sensors[sensor] = (beacon, distance_manhattan(*sensor, *beacon))

    logger.info(f'{os.getpid()=} {id(sensors):x} {id(test):x}')
    logger.debug(pformat(sensors))

def generate_xs(base, d):
    for x in range(-d, d+1):
        yield base + x

def solve(sensor, d, y):
    logger.debug(f'{sensor=} {d=} {y=}')
    d -= abs(sensor[1] - y)
    logger.debug(f'{d=}')
    
    if d > -1:
        return generate_xs(sensor[0], d)

def solve_y(y):
    global sensors
    
    for sensor, (beacon, d) in sensors.items():
        tmp = solve(sensor, d, y)
        if tmp:
            yield tmp
        logger.debug(f'{sensor=}, {beacon=}, {tmp=}')

def solve1(sensor, y):
    global sensors

    sensor, (beacon, d) = sensor
    xs = solve(sensor, d, y)
    logger.debug(f'{sensor=}, {beacon=}, {xs=}')

    if xs:
        # Remove overlapping xs, beacon xs and sensor xs
        xs = filter(lambda x: (x, args.y) not in sensors.keys(), xs)
        xs = filter(lambda x: (x, args.y) not in next(zip(*sensors.values())), xs)
        xs = set(xs)
        logger.info(f'{os.getpid()=} {id(sensors):x} {len(xs)=}')
        return xs
    else:
        return set()

def solve2(max_xy):
    # d - abs(target.y - sensor.y) - abs(target.x - sensor.x) < 0
    global sensors

    s = z3.Solver()

    x, y = z3.Ints('x y')
    s.add(x > -1)
    s.add(y > -1)
    s.add(x < int(max_xy)+1)
    s.add(y < int(max_xy)+1)

    for sensor, (_, d) in sensors.items():
        s.add(d < (z3.Abs(y - sensor[1]) + z3.Abs(x - sensor[0])))

    logger.debug(f'{s.check()=}')

    model = s.model()
    logger.debug(f'{s.model()[x]=}')

    return model[x].as_long(), model[y].as_long()

with args.inp as inp:
    ls = inp.read()

    read_sensors(ls)

    with ProcessPoolExecutor(initializer=read_sensors, initargs=(ls,)) as executor:
        worker = partial(solve1, y=args.y)

        xs = itertools.chain(*executor.map(worker, sensors.items()))
        xs = set(xs)
        logger.debug(f'{xs=}')
        print(len(xs))
    
    x, y = solve2(args.m)
    print(x * 4000000 + y)
