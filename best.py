import sys
import numpy as np
import vw
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

optimal = np.argmax(data[:,6])
optimal_model = int(data[optimal,0])
print "optimal model (area under pai)",optimal_model,"l1",data[optimal,1],"l2",data[optimal,2]
optimal2 = np.argmin(data[:,5])
print "optimal model (rmse)",int(data[optimal2,0]),"l1",data[optimal2,1],"l2",data[optimal2,2]

vw.plot_regularization(l1,"l1",1,name+mode_name+"-"+"lasso")
vw.plot_regularization(l2,"l2",2,name+mode_name+"-"+"ridge")
result.close()
