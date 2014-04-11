import sys
import vw
import numpy as np
import math
import matplotlib.pyplot as plt

# Expects [pred1,pred2, ... predn, actual,num_areas][pred1,pred2,...,predn,actual,num_areas]...[]


class PAIGroup():
    def __init__(self,group):
        self.num_areas = int(group[-1])
        self.actual = group[-2]
        self.pred = group[0:-2]

    def __str__(self):
        return "Actual:"+self.actual+" Pred:"+str(self.pred)+" areas:"+str(self.num_areas)

    

def parsePAI():
    params = " ".join(sys.argv[1:]).split("]")
    pai_groups = []
    for p in params:
        g = p.replace("[","").replace(" ","")
        if len(g) > 0:
            g = g.split(",")
            if len(g) < 3:
                raise ValueError("Unexpected number of inputs:"+str(len(g))+","+str(g))
            pai_groups.append(PAIGroup(g))
    return pai_groups


def pai(pred,actual,num_areas):
    # return a list of the average cumsum of the actual crime, ordered by the predicted area
    # "                the standard error of the above
    if len(pred) != len(actual):
        raise ValueError("Predicted and Actual lengths are not equal:"+str(len(pred))+"!="+str(len(actual)))
    num_times = len(pred)/num_areas
    # create an empty numpy array
    result = np.zeros((num_times,num_areas+1))
    for ts in range(num_times):
        a = ts * num_areas
        b = a + num_areas
        z = zip(pred[a:b],actual[a:b])
        z.sort(key = lambda x: x[0], reverse=True) # sort by pred, largest to smallest
        cum = np.cumsum([x[1] for x in z])
        result[ts,1:] = cum
    return result


     
        

groups = parsePAI()
for g in groups:
    print g
    actual = vw.read(g.actual)
    areas = g.num_areas
    for predfile in g.pred:
        pred = vw.read(predfile)
        result = pai(pred,actual,areas)
        m = np.mean(result,axis=0)
        m = m/m[-1]
        se = np.std(result,axis=0)/math.sqrt(result.shape[0])
        x = np.linspace(0,1,result.shape[1])
        plt.plot(x,m,label=predfile.replace(".pred",""))


plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=3, mode="expand", borderaxespad=0.)
plt.show()
        
        
        
        









