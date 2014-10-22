import numpy as np

def permute(num,rows=[],lst = []):
    if len(lst) >= num:
        rows.append(lst[:])
            
    else:
        lst.append(0)
        permute(num,rows,lst)
        lst.append(1)
        permute(num,rows,lst)
    if len(lst) > 0:
        lst.pop()
    return rows

       
class Factor:
    def __init__(self,variables):
        self.variables = variables
    

    def create(self):
        print " , ".join(self.variables)
        print "running create, variables",self.variables
        rows = permute(len(self.variables),rows=[],lst=[])
        result = []
        for row in rows:
            print row,
            value = raw_input("?")
            row.append("("+value+")")
            result.append(row)
        self.data = result

    ''' gets the value corresponding to the specfied permutation. '''
    def getValue(self,entries):
        for r in self.data:
            if r[0:-1] == entries:
                return r[-1]
        

    def merge_variables(self,first,second):
        new_vars = first[:]
        for var in second:
            if var not in first:
                new_vars.append(var)
        return new_vars
    ''' returns a new factor '''
    def multiply(self,f):
            scope = self.merge_variables(self.variables,f.variables) # I want a defined order
            result = Factor(scope)
            indxA = [scope.index(v) for v in self.variables]
            indxB = [scope.index(v) for v in f.variables]
            print "indxA",indxA
            print "indxB",indxB
           
            rows = permute(len(scope),rows=[],lst=[])
            for r in rows:
                valueA = self.getValue([r[i] for i in indxA])
                valueB = f.getValue([r[i] for i in indxB])
                value = str(valueA)+"*"+str(valueB)
                r.append(value)
            result.data = rows
            return result

    def __repr__(self):
        string = ",".join(self.variables)+"\n"
        for row in self.data:
            string += "["+",".join([str(x) for x in row])+"]\n"
        return string

f0 = Factor(["x"])
f0.create()
print f0
f1 = Factor(["x","y0"])
f1.create()
print f1

f2 = Factor(["x","y0","y1"])
f2.create()
print f2

f3 = f0.multiply(f1)
print f3
f4 = f3.multiply(f2)
print f4

