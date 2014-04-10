# reads the arrest data and cleans it up.
import csv

f = open("/home/finn/phd/data/Arrest05-13.csv","r")
o = open("/home/finn/phd/data/arrests2.csv","w")
reader = csv.reader(f)
wrong = 0
for row in reader:
    row = ['"'+x.replace(","," ").replace("#"," ").replace("(","").replace(")","").replace('"',"")+'"' for x in row]
    o.write("|".join(row)+"\n")
        
f.close()
o.close()

##lines = f.readlines()
##count = 0
##total = 0
##for line in lines:
##    line = line.split(",")
##    total +=1
##    if len(line) != 28:
##        count +=1
##        #print line
##        #break
##print count
##print total
##f.close()
