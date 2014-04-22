import vw
import numpy as np
from numpy import exp
import matplotlib.pyplot as plt
import sys

output = sys.argv[1]
rows = int(sys.argv[2])

xe = np.ones((rows,3))
x = np.random.uniform(size = (rows,2),low=-2.0,high=2.0)
xe[:,1:] = x
w = [3,-2,-1]
r = xe.dot(w) + np.random.normal(size=rows,loc=0,scale=1)
#r = r - mean(r)
g = (exp(r))/(1+exp(r))
y = (np.random.uniform(size=rows) <= g)
#plt.scatter(x[:,0],x[:,1],c = y)
#plt.xlabel("x1")
#plt.ylabel("x2")
#plt.show()

data = np.zeros((rows,3))
data[:,0] = y
data[:,1:] = x

vw_data = vw.toVW(data,mode="class")

out = open(output,"w")
for line in vw_data:
    out.write(line+"\n")
out.close()




