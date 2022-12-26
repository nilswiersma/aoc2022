import sys
import logging
import argparse
from pprint import pformat

parser = argparse.ArgumentParser()
parser.add_argument('inp', type=argparse.FileType('r'))
parser.add_argument('-v', '--verbose', action='count', default=0)
args = parser.parse_args()

logging.basicConfig(format='[%(levelname)s:%(name)s:%(lineno)d] %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING - args.verbose*10)

def lformat(ls):
    return ',\n'.join(str(l) for l in ls)

class CompareException(Exception):
    pass

def compare(r1, r2):
    assert isinstance(r1, list) and isinstance(r2, list) or not isinstance(r1, list) and not isinstance(r1, list)
    
    logger.debug(f'{r1=} {r2=}')

    # Deal with the case running out of list items
    exc = None
    if len(r1) < len(r2):
        logger.debug(f'{len(r1)=}, {len(r2)=}, ok')
        exc = CompareException(True)
    elif len(r2) < len(r1):
        logger.debug(f'{len(r1)=}, {len(r2)=}, nok')
        exc = CompareException(False)

    for e1, e2 in zip(r1, r2):
        if isinstance(e1, list) or isinstance(e2, list):
            if not isinstance(e1, list):
                e1 = [e1]
            if not isinstance(e2, list):
                e2 = [e2]

            compare(e1, e2)
        elif e1 < e2:
            logger.debug(f'{e1}, {e2}, ok')
            raise CompareException(True)
        elif e2 < e1:
            logger.debug(f'{e1}, {e2}, nok')
            raise CompareException(False)
        else:
            logger.debug(f'{e1}, {e2}, continue')
    
    if exc:
        raise exc

with args.inp as inp:
    ls = inp.readlines()
    r1 = None
    r2 = None
    
    answer1 = 0

    for idx, l in enumerate(ls):
        if idx % 3 == 0:
            r1 = eval(l)
        elif idx % 3 == 1:
            r2 = eval(l)
        elif idx % 3 == 2:
            logger.debug(f'{r1=}')
            logger.debug(f'{r2=}')
            try:
                compare(r1, r2)
            except CompareException as e:
                logger.debug(repr(e))
                if e.args[0]:
                    logger.info(f'{idx//3+1}')
                    answer1 += idx//3+1

    print(answer1)
    assert answer1 == 5557 or answer1 == 13
    
    div1 = [[2]]
    div2 = [[6]]
    queue = [eval(l.strip()) for l in ls if l.strip()]
    sorted_ = [ div1, div2 ]

    logger.debug('sorted_=\n' + lformat(sorted_))
    
    while queue:
        e1 = queue.pop()
        logger.debug(f'{e1=}')
        for idx, e2 in enumerate(sorted_):
            try:
                compare(e1, e2)
                sys.exit(-2)
            except CompareException as e:
                if e.args[0]:
                    logger.debug(f'{e1=} {e2=} good order, put before {e2=}')
                    sorted_ = sorted_[:idx] + [e1] + sorted_[idx:]
                    break
                else:
                    logger.debug(f'{e1=} {e2=} wrong order, keep going')
            
        if e1 not in sorted_:
            sorted_.append(e1)

        logger.debug('sorted_=\n' + lformat(sorted_))
    
    logger.info('sorted_=\n' + lformat(sorted_))
    logger.info(f'{sorted_.index(div1)=}, {sorted_.index(div2)=}')

    print((sorted_.index(div1)+1) * (sorted_.index(div2)+1))
