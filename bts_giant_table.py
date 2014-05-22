# this file reads in tables at a given aggregation level in the format you get from the BTS and joins them all together to create a giant table (super-wide)

# first line is a header, columns that start with TAB are duplicated across different files without corresponding to the same variables. In other words they should be renamed.

# read the ReadMe file to get the actual feature names

# now ... join should be done on tract, all other variables should match.

# super file will look like: tract, f1, f2, f3, ... f10,000

# now how will I do the merging - there are about 4368 tracts (Texas a a whole). I could get more instances by doing all states. (so as to get a good selection of features)
# are block groups globaly unique or only within state, county ...

# lets do this in a sparce format...

# I need to know how many block-groups there are - so read the id file. Then I need to know how many features I will have - so read all the readme files.

# then I can output model matrix format... (does it have to be numerical?), row, col, value.

import os
import csv

README = "ReadMe"
TAB = "TAB"
TRACT = "TRACT"

def getDataFile(readMeName):
    indx = readMeName.index(README)
    return readMeName[0:indx-1]+".csv"

def processReadMe(readMe,dataFileName,column_maps,featureFile,featureID):
    f = open(readMe,"r")
    ids = []
    for line in f.readlines():
        line = line.split(",")
        line = [x.strip('"') for x in line]
        
        if line[0].startswith(TAB):
            description = ":".join(line[1:])
            featureFile.write("{},{},{}".format(featureID,line[0],description))
            ids.append(featureID)
            featureID +=1
    f.close()
    column_maps[dataFileName]=ids # I make the assumption that columns are ordered in the ReadMe in the same way as they are in the data file.
    return featureID




class DataFileProcessor:
    def __init__(self, column_maps, data_files, outfile):
        self.column_maps = column_maps # maps filename to a list of featureIDs
        self.entries = 0 # the number of entries written to the matrix
        self.tract_to_row =  {} # maps each tract to a row
        self.nextUnallocatedRow = 1 # the next row that is yet to be allocated to a tractID
        self.outfile = outfile
        self.maxFeatureID = 0
    

    def process_all(self):
        for df in data_files:
            self.process(df)
            
        return (self.nextUnallocatedRow-1,self.maxFeatureID,self.entries)
    
    def process(self,datafile):
        with open(datafile,"r") as f:
            reader = csv.reader(f)
            first = True
            ids = self.column_maps[datafile]
            for table_row in reader:
                if first:
                    first = False
                    idcols, columns = self._parseHeader(table_row,ids)
                else:
                    state_county_tract = [table_row[i] for i in idcols]
                    key = ":".join(state_county_tract)
                    row = self.tract_to_row.get(key)
                    if not row:
                        row = self.nextUnallocatedRow
                        self.tract_to_row[key] = row
                        self.nextUnallocatedRow +=1
                        self.outfile.write("{} 1 {}\n".format(row,row))
                        #self.outfile.write("{} 1 {}\n".format(row,state_county_tract[0])) # would have been row,key if mm accepted strings # row, column, value
                        #self.outfile.write("{} 2 {}\n".format(row,state_county_tract[1])) # would have been row,key if mm accepted strings # row, column, value
                        #self.outfile.write("{} 3 {}\n".format(row,state_county_tract[2])) # would have been row,key if mm accepted strings # row, column, value
                        self.entries +=1
                    for indx, tableIndx in enumerate(columns):
                        featureID = ids[indx]
                        value = float(table_row[tableIndx])
                        if value != 0.0:
                            if featureID > self.maxFeatureID:
                                self.maxFeatureID = featureID
                            self.outfile.write("{} {} {}\n".format(row,featureID,value))
                            self.entries+=1
   
                                     
    def _parseHeader(self,header,ids):
        id_columns = ["STATE","COUNTY","TRACT"]
        id_indexes = [None]*len(id_columns)
        columns = []
        for indx,col in enumerate(header):
            for i,idcol in enumerate(id_columns):
                if idcol==col:
                    id_indexes[i] = indx
                    break
            
            if col.startswith(TAB):
                columns.append(indx)
             
        if len(columns) != len(ids):
            raise ValueError("Number of tables labled with {} is {}. Does not match number found in Readme {}".format(TAB,len(self.columns),len(self.ids)))
        return (id_indexes,columns)                  
                
                            
# for each file, I need a list of ids

column_maps = {}
                             
files = os.listdir(".")
featureID = 2 #  tract will be the first
featureFile = open("features.csv","w")
data_files = []
for f in files:
    if README in f:
        df = getDataFile(f)
        data_files.append(df)
        featureID = processReadMe(f,df,column_maps, featureFile,featureID)
                             

# at this point I know how many features (columns there are)
try:
    giant = open("giant_table.mm","w")
    giant.write("%%MatrixMarket matrix coordinate real general\n")
    tell = giant.tell() # current position in file
    giant.write("                                                    \n") # should be rows, columns, entries but we don't know all that yet.
    processor = DataFileProcessor(column_maps,data_files,giant)
    rows, columns, entries = processor.process_all()
    giant.seek(tell)
    giant.write("{} {} {}".format(rows,columns,entries))
    print rows, columns, entries
        
finally:
    giant.close()
    

    

    
        
        

