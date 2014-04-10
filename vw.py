import math
import numpy as np

def read(f):
    targets = open(f,"r")
    result = []
    while (True):
        line = targets.readline()
        if not line:
            break
        p = float(line)
        result.append(p)
    targets.close()
    return result


# lets try calculating the average of the roc-areas
def pai(pred, actual, num_areas):
    nperiods = len(pred)/num_areas
    total = 0
    for t in range(0,nperiods):
        p = pred[t*num_areas:(t+1)*num_areas]
        a = actual[t*num_areas:(t+1)*num_areas]
        area = roc(p,a)
        total+=area
    mean_area = total/float(nperiods)
    return mean_area


        
def area(y):
    return sum(y)/float(len(y))
    

def roc(pred, actual):
    paired = zip(pred,actual)
    paired.sort(key = lambda x: x[0],reverse=True)
    result = [p[1] for p in paired]
    c = np.cumsum(result)
    total = float(c[-1])
    normalized = [i/total for i in c]
    return area(normalized)
    

def rmse(pred, actual):
    total = 0
    for i in range(len(pred)):
        diff = pow(pred[i]-actual[i],2)
        total += diff
    mse = total/len(pred)
    return math.sqrt(mse)







    
    
