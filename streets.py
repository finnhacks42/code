from operator import itemgetter
from time import sleep
import dstk
import re


def sort_dict_by_value(d,reverse=False):
    ''' proposed in PEP 265, using  the itemgetter '''
    return sorted(d.iteritems(), key=itemgetter(1), reverse=True)

def find_suffix(text):
    suffix = ["TOLLWAY","ST","RD","AVE","DR","CIR","TR","CI","LN","BLVDE","BLVD","BLV","BL","PL","CT","EXPWY","EXPY","EXP","EXN","HWY","FRWY","FWY","PKWY","PKW","WAY","ROW","EXT","CROS","CROSSING"]
    for s in suffix:
        if text.endswith(s):
            name = text[0:len(text)-len(s)]
            suffix = s
            return [name+" "+suffix,name,suffix,True]
        
    if text.endswith("D"):
        name = text[0:-1]
        suffix = "DR"
        return [name+" "+suffix,name,suffix,True]
        
    if text.endswith("R"):
        name = text[0:-1]
        suffix = "RD"
        return [name+" "+suffix,name,suffix,True]
    return [text,text,"",False]

fix = {"1ST":"FIRST","2ND":"SECOND","3RD":"THIRD","4TH":"FOURTH","5TH":"FIFTH","6TH":"SIXTH","7TH":"SEVENTH","8TH":"EIGHT","9TH":"NINTH","10TH":"TENTH"}
def street_matches(street1, street2):
    s1 = find_suffix(street1.upper().replace(" ",""))[1]
    s2 = find_suffix(street2.upper().replace(" ",""))[1]
    for k in fix:
        if s1.endswith(k):
            s1 = s1[0:len(s1)-len(k)]+fix[k]
        if s2.endswith(k):
            s2 = s2[0:len(s2)-len(k)]+fix[k]
    
    if s1 == s2:
        return True
    # if they are the same at the start but one has one extra letter say they are the same
    else:
        if abs(len(s1)-len(s2))< 2:
            l = min(len(s1),len(s2))
            s1s = s1[0:l]
            s2s = s2[0:l]
            if s1s == s2s:
                return True
    
    return False
    
    

def number_difference(number1, number2):
    try:
        n1 = int(number1)
        n2 = int(number2)
        return abs(n1-n2)

    except ValueError:
        return "NA"

# looks for the value corresponding to the specified key. If it is not there or explicitly mapped to None, return alt value 
def dict_get(d, key, alt):
    value = d.get(key,alt)
    if not value:
        return alt
    return value
    

def geocode(address):

    address_string = str(address)
    geo = dstk.street2coordinates(address_string)[address_string]
    if geo == None:
        return ["NA"]*7
       
    else:
        lat = dict_get(geo,'latitude','NA')
        lon = dict_get(geo,'longitude','NA')
        street = dict_get(geo,'street_name','NA')
        conf = dict_get(geo,'confidence','NA')
        number = dict_get(geo,'street_number','NA')
        
        street_match = street_matches(street, address.street_and_dir)
        num_diff = number_difference(number,address.number)
    
        
    return [lat,lon,number,street,conf,num_diff,street_match]



class Address:
    
    def __init__(self,number,direction,street,zipcode,area):
        self.key=number+direction+street+area
        self.key = self.key.replace(" ","")
        number = number.lstrip("0").replace("xx","50")
        suffix = find_suffix(street)
        street = suffix[0]
        direction = direction.strip(" ")
        self.area = area
        self.number = number
        self.direction = direction
        self.street = street
        self.zipcode = zipcode
        
        if len(direction) > 0:
            self.street_and_dir = direction+" "+street
        else:
            self.street_and_dir = street
        self.string = number+" "+self.street_and_dir+" DALLAS TX"
            
    def __hash__(self):
        return hash(self.key)

    def __eq__(self,other):
        return self.key==other.key

    def __str__(self):
        return self.string
    def __repr(self):
        return self.string

def build_address_to_count_map(inputfile):
    f = open(inputfile,"r")
    address_to_crime = {}
    count = 0
    f.readline() # read the header
    while count < 500:
        line = f.readline()
        if not line:
            break
        line = line.split("\t")
        direction = line[18].strip('"')
        street = line[19].strip('"')
        block = line[17].strip('"')
        zipcode = line[23].strip('"')
        area = line[9].strip('"')
        address = Address(block,direction,street,zipcode,area)
        crime_count = address_to_crime.get(address)
        if crime_count == None:
            crime_count = 0
        address_to_crime[address] = crime_count + 1  
        #count +=1
    f.close()
    address_to_crime = sort_dict_by_value(address_to_crime,True)
    return address_to_crime



dstk = dstk.DSTK({'apiBase':'http://localhost:8080'})





zip_pattern = re.compile("[0-9]{5}")

    
address_counts = build_address_to_count_map("fixrawdata.txt")  



fixed = []
out = open("geocoded3.txt","w",1)
header=["count","key","reportingarea","lat","lon","number","street","geo_conf","number_diff","street_matches"]
out.write("|".join(output)+"\n")
for i in range(0,len(address_counts)): 
    print "Looking up:",i
    address = address_counts[i][0]
    count = address_counts[i][1]
    geo = geocode(address)
    output=[count,address.key,address.area]
    output.extend(geo)
    output = ['"'+str(x)+'"' for x in output]
    outstring = "|".join(output)+"\n"
    out.write(outstring)
    

out.close()
    
