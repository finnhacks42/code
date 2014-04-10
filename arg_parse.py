import sys
import vw
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
    result = np.zeros((num_times,num_areas))
    for ts in range(num_times):
        a = ts * num_areas
        b = a + num_areas
        z = zip(pred[a,b],actual[a,b])
        z = z.sort(key = lambda x: x[0], reverse=True) # sort by pred, largest to smallest
        cum = np.cumsum([x[1] for x in z])
        result[ts,:] = cum        
     
        

groups = parsePAI()
for pai in groups:
    print pai


