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
    
    

w = [-2] # intercept
w.extend(list(halvings(5))*2)

w.extend([0]*10)
w = np.transpose(w)

# 5 x values, drawn from unif(-1,1). 5 x vals = previous ones plus noise, 10 more independent x values in unif(-1,1) => 20 columns in all

# number of data points
n = 10000

m0 = np.ones((n,1)) #intercept
m1 = np.random.uniform(-1,1,size=(n,5))
noise = np.random.normal(0,.2,size=(n,5))
m2 = m1+noise
m3 = np.random.uniform(-1,1,size=(n,10))
# join [m1,m2,m3]
x = np.concatenate((m0,m1,m2,m3),axis=1)


# now take the dot product with w

added = np.dot(x,w)
risk = sigmoid(added)
y = np.reshape(bernouli(risk),(n,1))


header = ["target"]
header.extend([str(i+1) for i in range(20)])

h = ",".join(header)
data = np.concatenate((y,m1,m2,m3),axis=1) # note intercept is not included in output

train = data[0:1000,:]
test = data[1000:n,:]

np.savetxt("/home/finn/phd/data/logistic_train.csv",train,delimiter=",",header=h,comments='')
np.savetxt("/home/finn/phd/data/logistic_test.csv",test,delimiter=",",header=h,comments='')

vw.saveToVW("/home/finn/apps/vowpal_wabbit-7.4/finn/logistic_train",train,mode="regr")
vw.saveToVW("/home/finn/apps/vowpal_wabbit-7.4/finn/logistic_valid",test,mode="regr")








