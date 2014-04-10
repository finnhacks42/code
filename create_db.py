# databases the raw data
import sqlite3
import csv
import re
import sys
import datetime

# Assumptions
# The data is tab seperated
# NA/Null values are represented by whitespace
# Date and time formats are one of the few recognized by TypeGuru

# converts a string of the form mm/dd/yyyy to a datetime.date object.
def mmddyyyyToDate(dt):
    year = int(dt[6:])
    month = int(dt[0:2])
    day = int(dt[3:5])
    dto = datetime.date(year,month,day)
    return dto
    

def hhmmssToTime(time):
    hours = int(time[0:2])
    minutes = int(time[3:5])
    seconds = int(time[6:])
    totalseconds = hours*60*60+minutes*60+seconds
    return totalseconds

def hhmmToTime(time):
    hours = int(time[0:2])
    minutes = int(time[3:])
    totalseconds = hours*60*60+minutes*60
    return totalseconds

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def stringToUnicode(text):
    try:
        text.decode('utf-8')
        return result
    except ValueError:
        print "failed to convert,",text
        return ""

def toInteger(number):
    try:
        return int(number)
    except ValueError:
        return removeNonAscii(number)
    
    


# Tries to guess what type of thing a value is. Concepts supported date mm/dd/yyyy, time hh:mm, integer, text, real
class TypeGuru: #TODO make this return whitespace for pure whitespace
    def __init__(self):
        self.patterns = [re.compile(r"[0-9]{2}/[0-9]{2}/[0-9]{4}$"),re.compile(r"[0-9]{2}:[0-9]{2}:[0-9]{2}$"),re.compile(r"[0-9]{2}:[0-9]{2}$"),re.compile(r"-?[0-9]+$"),re.compile(r"-?[0-9.]+$"),re.compile(r"\s+$")]
        self.pnames = ["date","timehhmmss","timehhmm","integer","real","whitespace"]
        self.convertions = {"date":mmddyyyyToDate,"timehhmmss":hhmmssToTime, "timehhmm":hhmmToTime,"integer":toInteger,"real":float,"text":removeNonAscii}
        self.dbtype = {"date":"DATE","timehhmmss":"INTEGER","timehhmm":"INTEGER","integer":"INTEGER","text":"TEXT","real":"REAL"}
        # what to do to put the thing into an sql field and what kind of field
        self.default = "text"
    def getType(self,field):
        for indx,p in enumerate(self.patterns):
            if p.match(field):
                return self.pnames[indx]
        return self.default
    
    def convert(self,fieldType,value):
        function = self.convertions[fieldType]
        try:
            converted = function(value)
            return converted
        except ValueError:
            return value
        
    
    def getDBType(self, fieldType):
        return self.dbtype.get(fieldType)
    
        
        
    
def column_definitions(samplerows,per):
    guru = TypeGuru()
    header = samplerows[0]
    types = {}
    for c in range(len(header)):
        types[c]={}
    
    for row in samplerows[1:]:
        if len(row) != len(header):
            raise ValueError("number of columns in this row "+str(len(row))+" does not match header size: "+str(len(header)))
        for colID,col in enumerate(row):
            col = col.strip()
            fieldType = guru.getType(col)
            fieldForColumnCount = types[colID].get(fieldType)
            if not fieldForColumnCount:
                types[colID][fieldType] = 1
            else:
                types[colID][fieldType] = fieldForColumnCount + 1
    # now we validate the types found and check that they seem valid
    best_types = []
    for indx, column_name in enumerate(header):
        value = types[indx]
        missing_values = value.get("whitespace",0)
        best_count = 0
        best_type = "text"
        for fieldType,count in value.items():
            if "whitespace" != fieldType and count > best_count:
                best_count = count
                best_type = fieldType
        rows = len(samplerows)-1
        percentage = best_count/float(rows - missing_values)
        if percentage < per:
            best_type = "text"
        best_types.append(best_type)
    return (header,best_types)

def create_table(cursor,tablename,column_definitions):
    guru = TypeGuru()
    statement = 'CREATE TABLE '+tablename+' ('
    column_names = column_definitions[0]
    column_types = column_definitions[1]
    statements = []
    for i in range(len(column_names)):
        statements.append(column_names[i]+" "+guru.getDBType(column_types[i]))
    statement += ",".join(statements)+')'
    print statement
    cursor.execute(statement)
    



f = open(sys.argv[1],"r")
max_sample = 100
rownum = 0
samples = []
reader = csv.reader(f,delimiter="\t")


while rownum < max_sample:
    line = reader.next()
    if not line:
        break
    samples.append(line)
    rownum+=1
f.close()

conn = sqlite3.connect('crime.db',detect_types=sqlite3.PARSE_DECLTYPES)
c = conn.cursor()
columns = column_definitions(samples,1)
create_table(c,"crime",columns)

f = open(sys.argv[1],"r")
reader = csv.reader(f,delimiter="\t")
header = columns[0]
types = columns[1]
n_cols = len(header)
count = 0
fill_line = ",".join(["?"]*len(header))
guru = TypeGuru()
for line in reader:
    if count > 0:
        #insert the data
        converted = [0]*n_cols
        for i, field in enumerate(line):
            t = types[i]
            fixed = guru.convert(t,field)
            converted[i] = fixed
        statement = "INSERT INTO crime ("+",".join(header)+") VALUES ("+fill_line+")"
        #print statement
        c.execute(statement,converted)
        
    if count % 100000 == 0:
        print count
   
    count +=1

conn.commit()
conn.close() 




