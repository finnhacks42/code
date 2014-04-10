f = open("residential_burglary_2000_2005.txt","r")

keyToDays = {}
header = f.readline()
for line in f.readlines():
    line = line.split("|")
    key = line[0]
    day = int(line[1])
    lat = float(line[2])
    lon = float(line[3])
    if key not in keyToDays:
        keyToDays[key]=[day]
    else:
        keyToDays[key].append(day)

orders = {}
maxKey = ""
maxDays = 0
tauCounts  = {}
for key,days in keyToDays.iteritems():
    days.sort()
    taus = [days[i]-days[i-1] for i in range(1,len(days))]
    for t in taus:
        count = tauCounts.get(t)
        if not count:
            count = 0
        count +=1
        tauCounts[t] = count
    l = len(days)
    if l > maxDays:
        maxKey = key
        maxDays = l
    count = orders.get(l)
    if not count:
        count = 0
    count = count + 1
    orders[l]=count
print orders
    
print maxKey,keyToDays.get(maxKey)
for t,count in tauCounts.iteritems():
    print t,count



f.close()
