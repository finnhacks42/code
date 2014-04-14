import numpy as np
import vw
import sys

name = sys.argv[1]
mode_name = sys.argv[2]
output_name = name+mode_name+".result"

result = open(output_name,"r")
lines = result.readlines()
data = np.zeros((len(lines),7))
row = 0
for line in lines:
    line = line.strip().split(",")
    data[row,:] = line
    row +=1
l2 = data[data[:,1]==0]
l1 = data[data[:,2]==0]

vw.plot_regularization(l1,"l1",1,name+mode_name+"-"+"lasso")
vw.plot_regularization(l2,"l2",2,name+mode_name+"-"+"ridge")
       
        
