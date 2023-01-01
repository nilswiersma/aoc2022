import sys
import os
import logging
import argparse
import re
import time

from pprint import pprint, pformat
from functools import total_ordering

parser = argparse.ArgumentParser()
parser.add_argument('inp', type=argparse.FileType('r'))
parser.add_argument('-v', '--verbose', action='count', default=0)
args = parser.parse_args()

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.WARNING - args.verbose*10)

# https://regex101.com/r/t36i2e/1
regex = r"Valve (?P<valve>[A-Z]{2}) has flow rate=(?P<flowrate>\d+); tunnels? leads? to valves? (?P<nexts>(?:[A-Z]{2}[, ]{0,2})*)"

@total_ordering
class Valve():
    def __init__(self, name, flowrate, nexts):
        self.name = name
        self.flowrate = flowrate
        self.next_names = nexts
        self.nexts = None

    def __repr__(self):
        return f'<Valve@0x{id(self):x} {self.name} {self.flowrate} {self.next_names}>'
    
    def __eq__(self, other):
        return self.name == other.name
    
    def __lt__(self, other):
        return self.name < other.name
    
    def __hash__(self):
        return hash(repr(self))

def read_valves(ls):
    global valves

    valves = []

    for match in re.finditer(regex, ls, re.MULTILINE):
        valve = match.groupdict()['valve']
        flowrate = int(match.groupdict()['flowrate'])
        nexts = match.groupdict()['nexts'].split(', ')
        logger.debug(f'{os.getpid()=} {valve=} {flowrate=} {nexts=}')
        
        valves.append(Valve(valve, flowrate, nexts))

    for valve in valves:
        valve.nexts = list(filter(lambda x: x.name in valve.next_names, valves))

    logger.info(f'{os.getpid()=} 0x{id(valves):x}')
    logger.debug(f'{pformat(valves)}')

def calc_valve_paths():
    global valves
    global valve_paths 

    valve_paths = {}
    valves_with_flow = tuple(filter(lambda x: x.flowrate, valves))
    valve_start = next(filter(lambda x: x.name == 'AA', valves))

    for valve in (valve_start,) + valves_with_flow:
        # real score
        gscore = {}

        camefrom = {}
        openset = []

        for v2 in valves:
            gscore[v2] = sys.maxsize
        
        openset.append(valve)
        gscore[valve] = 0

        while openset:
            v = openset.pop(0)

            for n in v.nexts:
                score = gscore[v] + 1

                if score < gscore[n]:
                    camefrom[n] = v
                    gscore[n] = score

                    if not n in openset:
                        openset.append(n)
        
        valve_paths[valve] = {}
        for v2 in valves_with_flow:
            valve_paths[valve][v2] = gscore[v2]

def valve_str(valves):
    return ''.join(sorted([v.name for v in valves]))

def pressure_tick(vopen):
    return sum(map(lambda x: x.flowrate, vopen))

def maximum_additional_pressure(minute, valve, vopen):
    global valves

    minutes = 30 - minute + 1

    return sum(map(lambda x: x.flowrate * minutes, valves))

    # Maximum possible all open valves flowrate for the remaining minutes
    bound =+ sum(map(lambda x: x.flowrate * minutes, vopen))

    # + opening additional valves per 2 minutes in order of highest flowrate
    for valve in sorted(filter(lambda x: x not in vopen and x.flowrate > 0, valves), 
            key=lambda x: x.flowrate, reverse=True):
        bound += valve.flowrate * minutes
        minutes -= 2
        if minutes <= 1:
            break

    return bound

def reconstruct_path(camefrom, current):
    ret = [current]
    while current in camefrom.keys():
        current = camefrom[current]
        ret.append(current)
    return ret

def path_to_str(path):
    ret = ''
    for minute, valve, vopen in path[::-1]:
        ret += f'Minute {minute:2d} @ {valve.name}, release {pressure_tick(vopen):4d} pressure, open: {valve_str(vopen)}\n'
    return ret

def update(current, next_, score, gscore, camefrom, openset):
    if next_ not in gscore or score > gscore[next_]:
        camefrom[next_] = current
        gscore[next_] = score
        if next_ not in openset:
            openset.append(next_)

def solve1():
    global valves
    global valve_paths

    MAX_MINUTES = 30

    start = next(filter(lambda x: x.name == 'AA', valves))
    valves_with_flow = tuple(filter(lambda x: x.flowrate, valves))
    
    gscore = {}
    camefrom = {}
    openset = []

    init = (1, start, ())

    gscore[init] = 0
    openset.append(init)
    
    highest_gscore = 0
    highest_path = None

    t = time.time()
    while openset:
        # A* without heuristic, just use currently highest gscore
        # Take the state with the highest potential pressure
        current = sorted(openset, key=lambda x: gscore[x], reverse=True)[0]
        openset.remove(current)
        minute, valve, vopen = current

        logger.debug(f'{minute=} {len(openset)=} {valve.name=} {gscore[current]=} {valve_str(vopen)=}')
        if time.time() - t > 5:
            logger.info(f'{minute=} {len(openset)=} {valve.name=} {gscore[current]=} {valve_str(vopen)=}')
            t = time.time()
        
        # # Ignore this path if it will be lower than the current highest gscore
        # if gscore[current] + maximum_additional_pressure(*current) < highest_gscore:
        #     continue

        # Time's up
        if minute == MAX_MINUTES:
            if gscore[current] > highest_gscore:
                highest_gscore = gscore[current]
                highest_path = reconstruct_path(camefrom, current)
                logger.info(f'{highest_gscore=}')
            continue
        
        # Add option to stay and do nothing
        score = gscore[(minute, valve, vopen)] + (MAX_MINUTES - minute + 1) * pressure_tick(vopen)
        next_ = (MAX_MINUTES, valve, vopen)
        update(current, next_, score, gscore, camefrom, openset)
        
        # Add options to go to next unopened valve with flow and open it
        for valve_next in valves_with_flow:
            if valve_next not in vopen:
                minutes_to_valve_next = valve_paths[valve][valve_next]
                # Add one minute to open it
                minutes_to_valve_next += 1
                if minutes_to_valve_next < MAX_MINUTES - minute:
                    score = gscore[(minute, valve, vopen)] + minutes_to_valve_next * pressure_tick(vopen)
                    vopen_ = tuple(sorted((valve_next,) + vopen))
                    next_ = (minute + minutes_to_valve_next, valve_next, vopen_)
                    update(current, next_, score, gscore, camefrom, openset)

    logger.info(path_to_str(highest_path))
    print(f'{highest_gscore=}')

def solve2():
    global valves
    global valve_paths

    MAX_MINUTES = 26

    # (valve, vopen, vclosed, minutes, pressure, priority, debug)
    start = next(filter(lambda x: x.name == 'AA', valves))
    valves_with_flow = tuple(filter(lambda x: x.flowrate, valves))
    
    gscore = {}
    camefrom = {}
    openset = []

    init = (1, (start, start), ())

    gscore[init] = 0
    openset.append(init)
    
    highest_gscore = 0
    highest_path = None

    t = time.time()
    while openset:
        # A* without heuristic, just use currently highest gscore
        # Take the state with the highest potential pressure
        current = sorted(openset, key=lambda x: gscore[x], reverse=True)[0]
        openset.remove(current)
        minute, valves, vopen = current

        logger.debug(f'{minute=} {len(openset)=} {valve_str(valves)=} {gscore[current]=} {valve_str(vopen)=}')
        if time.time() - t > 5:
            logger.info(f'{minute=} {len(openset)=} {valve_str(valves)=} {gscore[current]=} {valve_str(vopen)=}')
            t = time.time()
        
        # # Ignore this path if it will be lower than the current highest gscore
        # if gscore[current] + maximum_additional_pressure(*current) < highest_gscore:
        #     continue

        # Time's up
        if minute == MAX_MINUTES:
            if gscore[current] > highest_gscore:
                highest_gscore = gscore[current]
                highest_path = reconstruct_path(camefrom, current)
                logger.info(f'{highest_gscore=}')
            continue
        
        # Add option to stay and do nothing
        score = gscore[(minute, valves, vopen)] + (MAX_MINUTES - minute + 1) * pressure_tick(vopen)
        next_ = (MAX_MINUTES, valves, vopen)
        update(current, next_, score, gscore, camefrom, openset)
        
        # Add options to go to next unopened valve with flow and open it
        valves_to_visit = filter(lambda v: v not in vopen, valves_with_flow)
        

        for valve_next in valves_with_flow:
            if valve_next not in vopen:
                minutes_to_valve_next = valve_paths[valve][valve_next]
                # Add one minute to open it
                minutes_to_valve_next += 1
                if minutes_to_valve_next < MAX_MINUTES - minute:
                    score = gscore[(minute, valve, vopen)] + minutes_to_valve_next * pressure_tick(vopen)
                    vopen_ = tuple(sorted((valve_next,) + vopen))
                    next_ = (minute + minutes_to_valve_next, valve_next, vopen_)
                    update(current, next_, score, gscore, camefrom, openset)

    logger.info(path_to_str(highest_path))
    print(f'{highest_gscore=}')

with args.inp as inp:
    ls = inp.read()
    read_valves(ls)
    calc_valve_paths()
    solve1()
