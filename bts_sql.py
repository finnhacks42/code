# join fields STATE,COUNTY,TRACT
import csv
import os
import sqlite3
import re
import numpy as np
# first parse all the readme files to get all the variable names

class ReadMe:
    def __init__(self):
        self.varMap = {}

    """ custom extract """
    def extract_key(self,name):
        if name.startswith("TAB"):
            name = name[3:].split("X")
            key = name[0].zfill(3)+name[1].zfill(3)
            return key
        else:
            return name
        
    def process(self, readMeList):
        for readMe in readMeList:
            with open(readMe,"r") as f:
                r = csv.reader(f,delimiter=",",quotechar='"')
                for row in r:
                    varName = row[0].replace(",","")
                    varDescription = row[1].replace(",",";")
                    self.set_description(varName,varDescription)
        self.variables = self.varMap.keys()
        self.variables.sort(key = self.extract_key)

    """ Set the description of the specified variable. Raises an error if the variables is already there with a different description (ignoring case)"""
    def set_description(self,varName,varDescription):
        desc = self.varMap.get(varName)
        if not desc:
            self.varMap[varName] = varDescription
        else:
            if desc.upper() != varDescription.upper():
                raise ValueError("Multiple descriptions for variable with the same name. {} vs {}".format(desc,varDescription))

    def getNames(self):
        return self.variables

    def getDescriptions(self):
        return [self.varMap[key] for key in self.variables]

class TypeSniffer:
    def __init__(self):
        self.empty = re.compile(r"\s+$")
        self.patterns = [self.empty,re.compile(r"-?[0-9]+$"),re.compile(r"-?[0-9.]+$")] # empty, integer, real
        self.types = ["EMPTY","INTEGER","REAL","TEXT"]
        self.typeMap = {} # #maps from variable name to type name
        self.rows = set([])

    """ Go through num_rows lines in the specified dataFile and determine the type for each column""" 
    def processForTypes(self,dataFileList,num_rows):
        num_rows = -1
        for dataFile in dataFileList:
            with open(dataFile,"r") as f:
                r = csv.reader(f,delimiter=",",quotechar='"')
                header = r.next()
                count = 0
                for row in r:
                    count +=1
                    if num_rows < 0 or count <= num_rows:
                        for i,value in enumerate(row):
                            self.set_type_from_value(header[i],value)
        varToType = {}                 
        for var,typeID in self.typeMap.iteritems():
            varToType[var] = self.types[typeID]
        self.typeMap = varToType
        
    def firstMatch(self,value):
        for i, pattern in enumerate(self.patterns):
            if pattern.match(value):
                return i
        return 3
                         
    """ Set the type of the specified variable"""
    def set_type_from_value(self,varName,value):
        prevIndx = self.typeMap.get(varName)
        if prevIndx == 3: # if the field is alreay marked text - do nothing it cannot change
            return
        if not prevIndx: # if its not already in the dictionary mark it as the easiset thing to override (empty)
            prevIndx = 0
        thisIndx = self.firstMatch(value)
        self.typeMap[varName]=max(thisIndx,prevIndx)

    def getTypeMap(self):
        return self.typeMap

    
        
class VarInfo:   
    def __init__(self, readMeList,dataList):
        readProc = ReadMe()
        readProc.process(readMeList)
        variables = readProc.getNames()
        descriptions = readProc.getDescriptions()
        sniffer = TypeSniffer()
        sniffer.processForTypes(dataList,100)
        typeMap = sniffer.getTypeMap()
        types = [typeMap.get(v) for v in variables]

        self.table_vars = []
        self.other_vars = []
        self.table_desc = []
        self.other_desc = []
        self.table_types = []
        self.other_types = []
        for i,variable in enumerate(variables):
            if variable.startswith("TAB"):
                self.table_vars.append(variable)
                self.table_desc.append(descriptions[i])
                self.table_types.append(types[i])
            else:
                self.other_vars.append(variable)
                self.other_desc.append(descriptions[i])
                self.other_types.append(types[i])
            

    """ writes out index, column name, column type, column description. First for all table type variables, then for the rest"""
    def write(self,filename):
        with open(filename,"w") as f:
            for i, variable in enumerate(self.table_vars):
                f.write("{},{},{},{}\n".format(i+1,variable,self.table_types[i],self.table_desc[i]))
            for i,variable in enumerate(self.other_vars):
                f.write("{},{},{},{}\n".format(i+len(self.table_vars)+1,variable,self.other_types[i],self.other_desc[i]))

    def getTableVarsMap(self):
        return dict(zip(self.table_vars,range(len(self.table_vars))))

    def getTableVars(self):
        return self.table_vars

""" We only need to check one file for the tracts, since they are the same for each data file"""


class MatrixBuilder:
    
    def __init__(self,data_files,varinfo):
        self.KEY_FIELDS = ["STATE","COUNTY","TRACT"]
        self.data_files = data_files
        self.tracts = self.getTracts()
        self.matrix, self.header = self.buildMatrix(varinfo)
        

    """ Not all files nessesarily have exactly the same tracts ..."""
    def getTracts(self):
        keys = set([])
        for dataFile in self.data_files:
            with open(dataFile,"r") as f:
                r = csv.reader(f,delimiter=",",quotechar='"')
                header = r.next()
                key_indx = [header.index(x) for x in self.KEY_FIELDS]
                for row in r:
                    key="".join([row[i] for i in key_indx])
                    keys.add(key)
        return dict(zip(keys,range(len(keys))))

    def buildMatrix(self,varinfo):
        variables = varinfo.getTableVarsMap()
        rows = len(self.tracts)
        columns = len(variables)+1 # 1 for the key
        column_lables = ["key"]
        column_lables.extend(varinfo.getTableVars())
        M = np.ones(shape=(rows,columns)) * -1 # use negative numbers for default
        for dataFile in self.data_files:
            seen = []
            with open(dataFile,"r") as f:
                r = csv.reader(f,delimiter=",",quotechar='"')
                header  = r.next()
                key_indx = [header.index(x) for x in self.KEY_FIELDS]
               
                table_indx = [i for i,name in enumerate(header) if name.startswith("TAB")]
                for row in r:
                    key = "".join([row[i] for i in key_indx])
                    try:
                        rowIndx = self.tracts[key]
                        seen.append(key)
                    except KeyError:
                        print key,"not in tracts"
                        continue
                    M[rowIndx,0] = key
                    for i in table_indx:
                        value = row[i]
                        if len(value) > 0:
                            value = float(value)
                            column_name = header[i]
                            col = variables[column_name]+1
                            M[rowIndx,col] = value
                                
            missing = 0
            for k in self.tracts.keys():
                if k not in seen:
                    missing +=1
                    #print k,"missing from file",dataFile
            if missing > 0:
                print missing,"tracts are missing from ",dataFile
            
        return M,column_lables

    def write(self,fileName):
        with open(fileName,"w") as f:
            headText = ",".join(self.header)
            f.write(headText+"\n")
            for row in self.matrix:
                output = []
                for col in row:
                    if col < 0:
                        output.append("NA")
                    else:
                        output.append(str(col))
                f.write(",".join(output)+"\n")
                        
            
        

    def getMatrix(self):
        return self.matrix
    
                        
# NOW CODE CLASSES THAT DO EACH KIND OF OUTPUT I WANT

# START WITH WRITING TO A 2D NUMPY ARRAY, which I can then save and load straight into R ...

files = os.listdir(".")
data_files = [x for x in files if x.endswith(".csv") and not x.endswith("_ReadMe.csv")]
readme_files = []
df = []
for x in data_files:
    name = x[0:-4]
    readme = name+"_ReadMe.csv"
    if readme not in files:
        print "Missing ReadMe file",readme
    else:
        df.append(x)
        readme_files.append(readme)

data_files = df

#data_files = data_files[0:2]
#readme_files = readme_files[0:2]


        
varinfo = VarInfo(readme_files,data_files)
varinfo.write("features.txt")

matrix = MatrixBuilder(data_files,varinfo)
matrix.write("giant_matrix.txt")
                
                


# read through all the data_files



##        def addData(self,dataFile,cursor,conn):
##        KEY_FIELDS = ["STATE","COUNTY","TRACT"]
##        with open(dataFile,"r") as f:
##            r = csv.reader(f,delimiter=",",quotechar='"')
##            header = r.next()
##            key_indx = [header.index(x) for x in KEY_FIELDS]
##            table_indx = [i for i,name in enumerate(header) if name.startswith("TAB")]
##            count = 0
##            for row in r:
##                columns = []
##                values = []
##                key = "".join([row[i] for i in key_indx])
##                for i in table_indx:
##                    column_name = header[i]
##                    value = row[i]
##                    if not self.isNull(value):
##                        columns.append(column_name)
##                        values.append(value)
##                if len(values) > 0:
##                    statement = "INSERT INTO {} (KEY,".format(self.tableName)+",".join(columns)+") VALUES ("+key+","+",".join(values)+");"
##                    try:
##                        cursor.execute(statement)
##                    except:
##                        print "FAILED TO EXECUTE:"+statement               
##        conn.commit()               

##    """ write out column indx, column name, column type, column description"""
##    def writeFeatures(self,filename):
##        dbtypes = self.getTypes()
##        with open(filename,"w") as f:
##            for key,value in self.varMap.iteritems():
##                f.write("{},{},{}\n".format(key,dbtypes.get(key),value))
##
##    def createTable(self,tableName, cursor):
##        dbtypes = {}
##        self.columns = {} # maps column name to the position of that column in the database
##        self.tableName = tableName
##        position = 1
##        for key,value in self.typeMap.iteritems():
##            if key.startswith("TAB"):
##                self.columns[key] = position
##                position +=1
##                dbtypes[key] = self.types[value]
##        
##        statement = "(KEY INTEGER"
##        for varname,columnType in dbtypes.iteritems():
##            statement += ","+varname+" "+columnType
##        statement +=");"
##        try:
##            cursor.execute("DROP TABLE {};".format(tableName))
##        except:
##            pass
##        
##        statement = "CREATE TABLE {} ".format(tableName)+statement
##        #print statement
##        cursor.execute(statement)
##
##    def isNull(self,value):
##        if len(value) == 0:
##            return True
##        if self.empty.match(value):
##            return True
##        if float(value) == 0:
##            return True
##        return False
##    
##    def addData(self,dataFile,cursor,conn):
##        KEY_FIELDS = ["STATE","COUNTY","TRACT"]
##        with open(dataFile,"r") as f:
##            r = csv.reader(f,delimiter=",",quotechar='"')
##            header = r.next()
##            key_indx = [header.index(x) for x in KEY_FIELDS]
##            table_indx = [i for i,name in enumerate(header) if name.startswith("TAB")]
##            count = 0
##            for row in r:
##                columns = []
##                values = []
##                key = "".join([row[i] for i in key_indx])
##                for i in table_indx:
##                    column_name = header[i]
##                    value = row[i]
##                    if not self.isNull(value):
##                        columns.append(column_name)
##                        values.append(value)
##                if len(values) > 0:
##                    statement = "INSERT INTO {} (KEY,".format(self.tableName)+",".join(columns)+") VALUES ("+key+","+",".join(values)+");"
##                    try:
##                        cursor.execute(statement)
##                    except:
##                        print "FAILED TO EXECUTE:"+statement               
##        conn.commit()
##
##    def writeData(self,dataFile,out):
##        KEY_FIELDS = ["STATE","COUNTY","TRACT"]
##        with open(dataFile,"r") as f:
##            r = csv.reader(f,delimiter=",",quotechar='"')
##            header = r.next()
##            key_indx = [header.index(x) for x in KEY_FIELDS]
##            table_indx = [i for i,name in enumerate(header) if name.startswith("TAB")]
##            count = 0
##            for row in r:
##                columns = []
##                values = []
##                key = "".join([row[i] for i in key_indx])
##                for i in table_indx:
##                    column_name = header[i]
##                    value = row[i]
                    
        
        
                    
                    
                    
            
                
        
        
#   INSERT INTO table_name (column1,column2,column3,...)
#VALUES (value1,value2,value3,...);     
        


#    cur.execute("INSERT INTO Cars VALUES(8,'Volkswagen',21600)")      




    

#conn = sqlite3.connect('ctpp.db',detect_types=sqlite3.PARSE_DECLTYPES)
#c = conn.cursor()
#varInfo.createTable("p2",c)
#for i,f in enumerate(data_files):
#    varInfo.addData(f,c,conn)
#    print "Added file {} of {}".format(i,len(data_files))
#conn.close()

    


              
