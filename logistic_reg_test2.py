# a really simple logistic regression data set
import numpy as np
import math
import vw

def halvings(n):
    num = 1
    count = 0
    while count < n:
        yield 1.0/num
        num = num*2
        count +=1

def sigmoid(lst):
    return [1.0/(1+math.exp(-x)) for x in lst]

def bernouli(plst):
    r = np.random.uniform(0,1,len(plst))
    y = r < plst
    return y.astype(int)
        
# y = sigmoid(w.T*X)

n = 1000 # number of rows of data
c = 30 # number of columns (excluding intercept)
m0 = np.ones((n,1)) #intercept column
m1 = np.random.uniform(-1,1,size=(n,c)) #other columns
X = np.concatenate((m0,m1),axis=1)


w = [-2]# intercept weight

w.extend(list(halvings(c))) #other weights
w = np.transpose(w)

product = np.dot(X,w) # the linear combination w.T*X

risk = sigmoid(product)

y = np.reshape(bernouli(risk),(n,1))



data = np.concatenate((y,m1),axis=1) # note intercept is not included in output
train = data[0:n/2,:]
test = data[n/2:n,:]

header = ["target"]
header.extend([str(i+1) for i in range(c)])
h = ",".join(header)
np.savetxt("/home/finn/phd/data/logistic_train.csv",train,delimiter=",",header=h,comments='')
np.savetxt("/home/finn/phd/data/logistic_test.csv",test,delimiter=",",header=h,comments='')

vw.saveToVW("/home/finn/apps/vowpal_wabbit-7.4/finn/logistic_train",train,mode="class",namespace=True)
vw.saveToVW("/home/finn/apps/vowpal_wabbit-7.4/finn/logistic_valid",test,mode="class",namespace=True)

         
