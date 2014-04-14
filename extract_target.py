# extracts the target from the source file to a separate target file

import sys

f = open(sys.argv[1],"r")
o = open(sys.argv[1]+".target","w")

while True:
	line = f.readline()
	if not line:
		break
	s = line.index("|")
	target = float(line[0:s])
	o.write(str(target)+"\n")

f.close()
o.close()
