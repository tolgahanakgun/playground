from itertools import chain, product
import sys
import string

if len(sys.argv) == 4:
	charset = sys.argv[1]
	minlenght = sys.argv[2]
	maxlength = sys.argv[3]
else:
	print('Supply 3 arguements')
	print('Usage: permute.py charset minlenght maxlength')
	print('Example: permute abcdefghijklmnopqrstuvwxyz 2 4 -> will generate all 2 3 4 permutations of ascii lowercase')
	sys.exit(0)

def permute(charset, minlenght,maxlength):
    return (''.join(candidate)
        for candidate in chain.from_iterable(product(charset, repeat=i)
        for i in range(minlenght, maxlength + 1)))

for attempt in permute(charset, int(minlenght), int(maxlength)):
    print(attempt)