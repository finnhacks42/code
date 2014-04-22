import numpy as np
import sys
fname = sys.argv[1]
f = open(fname,"r")
tmp = open("tmp","w")
for line in f.readlines():
	y = 1.0/(1+np.exp(-1*float(line)))
	tmp.write(str(y)+"\n")
f.close()
tmp.close()
os.rename("tmp",fname)
