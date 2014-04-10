
def difference(raw_number,number):
    try:
        number_diff = abs(int(raw_number)-int(number))
        return number_diff
    except ValueError:
        return "NA"

streets = {}
f = open("geocoded_all.txt","r")
lines_read = 0
for line in f.readlines():
    lines_read +=1
    if lines_read % 10000 == 0:
        print "read",lines_read
    line = line.strip().split("|")
    raw = line[0] # this is the street and number before we fixed it
    fixed = line[1] # this is the full address we looked up.
    lat = line[2]
    lon = line[3]
    street_matches = 0
    number_matches = 0
    street = line[5].upper() 
    street_nospace = street.replace(" ","")
    number = line[4]
    conf = line[6]
    raw_parts = raw.split(" ")
    number_diff = "NA"
    
    if len(raw_parts) == 2:
        raw_street = raw_parts[1]
        raw_number = raw_parts[0]
        if raw_street == street_nospace:
            street_matches = 1
        if raw_number == number:
            number_matches = 1
    
        
        number_diff = difference(raw_number,number)
    returned_address = number+" "+street
    if street == "NONE":
        returned_address = "NA"
    data = [fixed,returned_address,street_matches,number_matches,number_diff, lat,lon,conf]
    #data = [fixed,lat,lon,number +" "+street,conf]
    data = ['"'+str(x)+'"' for x in data]
    streets[raw] = data   
f.close()
print "read in geo data"

f = open("fixrawdata.txt","r")
o = open("rawwithgeo.txt","w")
#header = ["cleaned_address","lat","lon","returned_address","geo_conf"]
header = ["cleaned_address","returned_address","street_matches","number_matches","number_diff","lat","lon","geo_conf"]
na = ['"NA"']*8
h = f.readline().strip().split("\t")
h.extend(header)

o.write("\t".join(h)+"\n")
count = 1
lines_read = 0
while count < 5:
    lines_read +=1
    if lines_read % 100000 == 0:
        print lines_read
    line = f.readline()
    if not line:
        break
    line = line.strip().split("\t")
    street = line[19].strip('"')
    block = line[17].strip('"').lstrip("0").replace("xx","50")
    street = block+" "+street
    geo = streets.get(street)
    if not geo:
        line.extend(na)
    else:
        line.extend(geo)
    o.write("\t".join(line)+"\n")
    #count +=1
o.close()

print "Done"
    

