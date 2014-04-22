import math
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

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

""" Applies the sigmoid function to all the entries in the specified file"""
def sigmoid_file(fname):
	f = open(fname,"r")
	tmp = open("tmp","w")
	for line in f.readlines():
		y = 1.0/(1+np.exp(-1*float(line)))
		tmp.write(str(y)+"\n")
	f.close()
	tmp.close()
	os.rename("tmp",fname)


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

def meanPaiArea(pred,actual,num_areas):
    pais = pai(pred,actual,num_areas)
    m = np.mean(pais,axis=0)
    m = m/m[-1]
    a = area(m)
    return a
        
    
        
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
    if len(pred) != len(actual):
	raise ValueError("Predicted and actual lengths differ:"+str(len(pred))+" vs "+str(len(actual)))
    total = 0
    for i in range(len(pred)):
        diff = pow(pred[i]-actual[i],2)
        total += diff
    mse = total/len(pred)
    return math.sqrt(mse)

# excpects a data frame with each row containing information on the performance of a vw model.
# columns 3-6 are assumed to be train-rmse, train-pai, test-rmse, test-pai
def plot_regularization(subset,xlabel,xcol,title):
    x = subset[:,xcol]
    figure, ax_array = plt.subplots(2,sharex=True)
    ax_array[0].semilogx(x,(subset[:,3]),label="train")
    ax_array[0].semilogx(x,(subset[:,5]),label="test")
    ax_array[1].semilogx(x,1-subset[:,4],label="train")
    ax_array[1].semilogx(x,1-subset[:,6],label="test")
    ax_array[0].set_ylabel("rmse")
    ax_array[1].set_ylabel("1 - area-under-pai")
    ax_array[0].set_title(title)
    ax_array[1].set_xlabel(xlabel)
    ax_array[0].legend(loc=2, borderaxespad=0.)
    plt.savefig(title+".png")
    plt.show()






    
    
