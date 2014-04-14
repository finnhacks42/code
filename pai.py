import sys
from vw import *
import numpy as np
import math
import matplotlib.pyplot as plt

# Expects [pred1,pred2, ... predn, actual,num_areas][pred1,pred2,...,predn,actual,num_areas]...[]

groups = parsePAI()
for g in groups:
    actual = read(g.actual)
    areas = g.num_areas
    for predfile in g.pred:
        pred = read(predfile)
        result = pai(pred,actual,areas)
        m = np.mean(result,axis=0)
        m = m/m[-1]
        se = np.std(result,axis=0)/math.sqrt(result.shape[0])
        x = np.linspace(0,1,result.shape[1])
        plt.plot(x,m,label=predfile.replace(".pred",""))


plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=3, mode="expand", borderaxespad=0.)
plt.show()
        
        
        
        









