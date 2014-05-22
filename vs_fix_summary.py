f = open("summary","r")
o = open("summary.fixed","w")
while True:
    line = f.readline()
    if not line:
        break
    line = line.split(",")
    end = line[-2:]
    start = line[0:-2]
    start = ":".join(start).replace(",",":")
    result = [start]
    result.extend(end)
    o.write(",".join(result))
    
   

f.close()
o.close()
