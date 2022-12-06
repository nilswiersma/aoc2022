import sys

marker_size = int(sys.argv[2])

with open(sys.argv[1], 'r') as inp:

    l = inp.readline()
    
    while l:
        l = l.strip()
        
        marker = l[:marker_size]
        
        marker_end = marker_size 
        while len(set(marker)) != len(marker):
            marker = l[marker_end-marker_size:marker_end]
            marker_end += 1

        print(marker, marker_end-1)

        l = inp.readline()
