# just prints the number of columns in a tab separated file
import sys

f = open(sys.argv[1],"r")
head = f.readline()
length = len(head.split("\t"))
print "Length:",length
line_number = 0
while True:
    line_number +=1
    line = f.readline()
    if not line:
        break
    l = len(line.split("\t"))
    if l != length:
        print line_number,l
        print line


f.close()
