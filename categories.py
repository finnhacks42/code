import re
f = open("fixrawdata.txt","r")
missing = "null" #encode any missing or illegal values with this


rp = {"AGGRAVATED":"AGG","FAMILY VIOLENCE":"FV","CLASS A":"MA","CRIMINAL":"CRIM","MISCHEIF":"MISCHIEF"}


count = 0
while count < 10:
    line = f.readline()
    if not line:
        break
    line = line.split("\t")
    descrip = re.sub("[().\/]*","",line[4]).strip()
    dbackup = descrip[:]
    changed = False
    for r in rp:
        if r in descrip:
            descrip = descrip.replace(r,rp.get(r))
            changed = True
    

    family = line[38].strip()
    if "ASSULT" in descrip:
        if "FV" in descrip and family != '"Y"':
            print descrip,family
        if "FV" not in descrip and family != '"N"':
            print descrip,family
        
        
        
    
    


print "done"
