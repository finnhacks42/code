import simplekml as kml
f = open("/home/finn/phd/data/journeys.csv","r")
output = kml.Kml()

def addToKml(output,line):
    #print line
    #first element of the line is the id
    coords = []
    do_output = False
    for i in range(1,len(line)-1,2):
        if float(line[i]) > 148:
            do_output = True 
            coords.append(( "%f.1f"%float(line[i]),"%f.1f"%float(line[i+1])))
            #output.newpoint(name=line[0],coords=[(line[i],line[i+1])])
    if do_output:
        output.newlinestring(name=line[0],coords = coords)
    return do_output

count = 0
for line in f.readlines():
    line = line.strip("\n").split(",")
    if len(line) > 10:
        result = addToKml(output,line)
        if result:
            count +=1
        if count > 10:
            break
    
                    
output.save("/home/finn/phd/data/tweet_journeys.kml")
print "Done"
f.close()

