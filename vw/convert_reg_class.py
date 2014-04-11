# converts a regression problem into a classification one by replacing any non-zero target variables with a 1

import sys

f = open(sys.argv[1],"r")
o = open(sys.argv[1]+"class","w")

while True:
	line = f.readline()
	if not line:
		break
	s = line.index("|")
	target = float(line[0:s])
	if target > 0:
		newtarget = 1
	else:
		newtarget = 0
	
	line = str(newtarget)+" "+line[s:]
	o.write(line)

f.close()
o.close()
