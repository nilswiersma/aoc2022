#!/usr/bin/python3

import os
import sys
import requests
from pathlib import Path

day = int(sys.argv[1])

url = f'https://adventofcode.com/2022/day/{day}/input'

resp = requests.get(url, headers={'Cookie': os.environ['AOC_COOKIE']})

assert resp.status_code == 200, resp.status_code

out_dir = Path(f'{day:03d}/data')
out_dir.mkdir(parents=True, exist_ok=True)

with open(out_dir / 'input', 'w') as outf:
    outf.write(resp.text)

