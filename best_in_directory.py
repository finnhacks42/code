# goes through all the predictions in a directory and orders them by pai and rmse.
# print the best for each type
import sys
import os
import vw
import re

p = re.compile("(.*[^0-9]{1})([0-9]{1,3})(.pred)")

target = sys.argv[1]
num_areas = int(sys.argv[2])
actual = vw.read(target)

result = {}
for filename in os.listdir("."):
	m = re.match(p,filename)
	if m:
		print "assessing",filename
		pred = vw.read(filename)
		pai = vw.meanPaiArea(pred,actual,num_areas)
		subset = m.group(1)
		prev_pai = result.get(subset)
		if not prev_pai or pai > prev_pai[1]:
			result[subset] = (filename,pai)

for subset in result:
	print subset,result[subset]


 
		

