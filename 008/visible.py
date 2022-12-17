import sys
import numpy

debug = False

with open(sys.argv[1], 'r') as inp:
    forest = []

    l = inp.readline().strip()
    while l:
        tl = [int(x) for x in l]
        forest.append(tl)

        l = inp.readline().strip()
    
    forest = numpy.array(forest)
    
    # part 1
    def parse_forest(forest):
        visible = numpy.zeros(forest.shape, dtype=int)
        for tl_idx, tl in enumerate(forest):
            largest_t = -1
            for t_idx, t in enumerate(tl):
                if t > largest_t:
                    largest_t = t
                    visible[tl_idx][t_idx] = 1
                if t == 9:
                    break
        if debug:
            print(forest)
            print(visible)
        return visible

    # Parse the forest left to right from four angles
    visible = numpy.zeros(forest.shape, dtype=int)
    
    for idx in range(4):
        visible = visible | numpy.rot90(parse_forest(
            numpy.rot90(forest, k=idx)), k=-1*idx)

    if debug:
        print()
        print(forest)
        print(visible)

    print(visible.sum())

    # part 2
    debug = False
    
    # Parse the forest left to right from four angles for all trees
    score = numpy.zeros(forest.shape, dtype=int)
    score.fill(1)
    
    def parse_forest2(forest):
        score = numpy.zeros(forest.shape, dtype=int)
        
        for tl_idx in range(forest.shape[0]):
            for t_idx in range(forest.shape[1]-1):
                tl = list(forest[tl_idx][t_idx:])
                tc = tl.pop(0)
                count = 0
                while tl:
                    tn = tl.pop(0)
                    count += 1
                    if tc <= tn:
                        break
                score[tl_idx][t_idx] = count
        return score

    for idx in range(4):
         score = score * numpy.rot90(parse_forest2(
            numpy.rot90(forest, k=idx)), k=-1*idx)
    
    if debug:
        print(forest)
        print(score)
    
    print(score.max())
