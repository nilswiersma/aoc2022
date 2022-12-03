import sys

score_table1 = {
        'A X': 1 + 3,
        'A Y': 2 + 6,
        'A Z': 3 + 0,
        'B X': 1 + 0,
        'B Y': 2 + 3,
        'B Z': 3 + 6,
        'C X': 1 + 6,
        'C Y': 2 + 0,
        'C Z': 3 + 3,
    }

score_table2 = {
        'A X': 3 + 0,
        'A Y': 1 + 3,
        'A Z': 2 + 6,
        'B X': 1 + 0,
        'B Y': 2 + 3,
        'B Z': 3 + 6,
        'C X': 2 + 0,
        'C Y': 3 + 3,
        'C Z': 1 + 6,
    }

def score(inp, score_table):
    lines = inp.readlines()
    scores = [score_table[x.strip()] for x in lines]
    score = sum(scores)
    print(f'{score=}')

with open(sys.argv[1], 'r') as inp:
    score(inp, score_table1)
    inp.seek(0)
    score(inp, score_table2)

