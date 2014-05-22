# logistic regression dummy data set
import numpy as np
import math
import vw

def sigmoid(lst):
    return [1.0/(1+math.exp(-x)) for x in lst]

def bernouli(plst):
    r = np.random.uniform(0,1,len(plst))
    y = r < plst
    return np.reshape(y.astype(int),(len(y),1))

n = 100
w = (np.array([.1, 0.5, 0.2]))
c1 = np.ones((n,1))
c2 = np.random.uniform(0,1,size=(n,1))
c3 = -1*c2+np.random.normal(0,0.6,size=(n,1))
x = np.concatenate((c1,c2,c3),axis=1)

risk = sigmoid(np.dot(x,w))
#y = np.reshape(bernoulli(risk),(n,1))

y= bernouli(risk)

data = np.concatenate((y,c2,c3),axis=1) # intercept is not included in output
train = data[0:n/2,:]
test = data[n/2:n,:]

header = ["target"]
header.extend([str(i+1) for i in range(2)]) # label the two columns
h = ",".join(header)
np.savetxt("/home/finn/phd/data/logistic_train.csv",train,delimiter=",",header=h,comments='')
np.savetxt("/home/finn/phd/data/logistic_test.csv",test,delimiter=",",header=h,comments='')

vw.saveToVW("/home/finn/apps/vowpal_wabbit-7.4/finn/logistic_train",train,mode="class",namespace=False)
vw.saveToVW("/home/finn/apps/vowpal_wabbit-7.4/finn/logistic_valid",test,mode="class",namespace=False)

