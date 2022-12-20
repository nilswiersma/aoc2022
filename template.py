import sys
import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('inp', type=argparse.FileType('r'))
parser.add_argument('-v', '--verbose', action='count', default=0)
args = parser.parse_args()

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.WARNING - args.verbose*10)

with args.inp as inp:
    l = inp.readline()
    while l:
        l = l.strip()
        logger.debug(l)

        pass

        l = inp.readline()
