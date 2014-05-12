# convert VW to GLM sparse input (matrix market format)
import re

def readVWLine(line):
    line = line.split("|")
    target = float(line[0])
    namespaces = [x.strip().split(" ") for x in line[1:]]
    return (target,namespaces) 

def getColumnAndRowCounts(name):
    f = open(name,"r")
    ns_size = {}
    rows = 0
    firstLine = True
    spaces = []
    while True:
        line = f.readline()
        if not line:
            break
        rows +=1
        #line = line.split("|")
        #target = float(line[0])
        #namespaces = [x.strip().split(" ") for x in line[1:]]
        namespaces = readVWLine(line)
        print namespaces
        for ns in namespaces:
            if firstLine:
                spaces.append(ns[0])
            if len(ns) > 1:
                name = ns[0]
                first = int(ns[1].split(":")[0])
                last = int(ns[-1].split(":")[0])
                size = ns_size.get(name,[10^9,0])
                if first < size[0]:
                    size[0] = first
                if last > size[1]:
                    size[1] = last
                ns_size[name]=size
        firstLine = False
        
    f.close()

   
        
    
    return (rows,ns_size,spaces)

def expandNS(namespace):
    # pull out column, value pairs
    for indx,ns in namespace.iteritems():
        for pair in ns[1:]:
            pair = pair.split(":")
            key = int(pair[0])
            value = float(pair[1])


def writeMM(name, outname):
    o = open(outname,"w")
    o.write("%%MatrixMarket matrix coordinate real general\n")
    tell = o.tell()
    print o.tell()
    o.write(" "*35+"\n")
    f = open(name,"r")
    row = 1
    maxcol = 0
    entries = 0
    while True:
        line = f.readline()
        if not line:
            break
        target,namespaces = readVWLine(line)
        if target != 0.0:
            entries +=1
            o.write(str(row)+" 1 "+str(target)+"\n")
        for ns in namespaces:
            for pair in ns[1:]:
                pair = pair.split(":")
                column = int(pair[0])+1
                if column > maxcol:
                    maxcol = column
                value = float(pair[1])
                o.write(str(row)+" "+str(column)+" "+str(value)+"\n")
                entries +=1
        row +=1
    
    print row,maxcol,entries
    o.seek(tell)
    o.write(str(row)+" "+str(maxcol)+" "+str(entries))
    f.close()
    o.close()

name = "/home/finn/phd/data/20140505/VW1000bgvalid"
outname = name+".mm"


writeMM(name,outname)



               





