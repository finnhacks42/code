# this program just does a search for table names in the text of a file
import sys
import re

pattern = re.compile("TAB[0-9]{1,4}X[0-9]{1,4}")
filename = sys.argv[1]
variables = []
with open(filename,"r") as f:
    while True:
        line = f.readline()
        if not line:
            break
        
        matches = pattern.findall(line)
        for m in matches:
            variables.append(m)

output = ['"'+var+'"' for var in variables]
print ",".join(output)
