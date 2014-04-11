import vw
import os
import sys

test_file = sys.argv[1]
test = vw.read(test_file)
testname = test_file.replace("valid.target","")
print testname

results = []
files = os.listdir(".")

for f in files:
	if f.endswith(".pred") and f.startswith(testname):
		pred = vw.read(f)
		error = vw.rmse(test,pred)
		pair = (f,error)
		results.append(pair)
		

results.sort(key = lambda x: x[1],reverse=False)
for r in results:
	print r


