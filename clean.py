f = open("fixrawdata.txt","r")
missing = "null" #encode any missing or illegal values with this


count = 0
while count < 10:
    line = f.readline()
    if not line:
        break
    line = line.split("\t")

    off_date = line[2]
    rep_date = line[3]
    


print "done"



    
    
    
