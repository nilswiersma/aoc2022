import sys
import logging
import argparse
from pprint import pformat

parser = argparse.ArgumentParser()
parser.add_argument('inp', type=argparse.FileType('r'))
parser.add_argument('factor', type=int)
parser.add_argument('rounds', type=int)
parser.add_argument('-v', '--verbose', action='count', default=0)
args = parser.parse_args()

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.WARNING - args.verbose*10)

m = -1 # reduction factor (product of all moduli) 

class Monkey():
    def __init__(self, _id):
        self.id = _id
        self.targets = [-1, -1]
        self.inspect = 0
    
    def test(self, val):
        return val % self.div == 0

    def throw(self, monkeys):
        self.inspect += 1
        item = self.items.pop(0)
        level = self.op(item)
        level = level // args.factor
        level = level % m
        target = self.targets[self.test(level)]
        monkeys[target].items.append(level)
        logger.debug(f'{self.id=} {level=} {target=}')

    def __repr__(self):
        return f'Monkey {self.id} {self.inspect} {self.items}'

with args.inp as inp:
    monkeys = []
    l = inp.readline()
    while l:
        l = l.strip()

        if l.startswith('Monkey'):
            _id = l.split(' ')[1].split(':')[0]
            monkeys.append(Monkey(_id))
        elif l.startswith('Start'):
            items = l.split(':')[1]
            items = items.replace(' ', '')
            items = items.split(',')
            monkeys[-1].items = [int(x) for x in items]
        elif l.startswith('Operation'):
            try:
                val = int(l.split(' ')[-1])
                if '+' in l:
                    monkeys[-1].op = lambda old, val=val: old + val 
                elif '*' in l: 
                    monkeys[-1].op = lambda old, val=val: old * val
                else:
                    raise Exception()
            except ValueError:
                monkeys[-1].op = lambda old: old * old
        elif l.startswith('Test'):
            val = int(l.split(' ')[-1])
            monkeys[-1].div = val
        elif l.startswith('If true'):
            val = int(l.split(' ')[-1])
            monkeys[-1].targets[True] = val
        elif l.startswith('If false'):
            val = int(l.split(' ')[-1])
            monkeys[-1].targets[False] = val
        else:
            pass

        l = inp.readline()
    
    logger.info(pformat(monkeys))
    
    m = 1
    for monkey in monkeys:
        m *= monkey.div
    logger.info(f'{m=}')

    for round in range(args.rounds):
        logger.info(f'{round=}')
        for monkey in monkeys:
            while monkey.items:
                monkey.throw(monkeys)

        logger.debug(pformat(monkeys))
    logger.info(pformat(monkeys))
    
    monkey_business = sorted([x.inspect for x in monkeys])
    logger.info(monkey_business)
    print(monkey_business[-1] * monkey_business[-2])
