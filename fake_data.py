# generates some nice fake data.
import random
import matplotlib.pyplot as plt
import numpy as np

# returns the number of crimes we get by flipping a biased coin n times. 
def binome_draw(coinWeight, n):
    count = 0
    for i in range(n):
        r = random.uniform(0,1)
        if r < coinWeight:
            count +=1
    return count

def binome(coinWeight, n,trials):
    total = 0
    for i in xrange(trials):
        total += binome_draw(coinWeight,n)
    total = total/float(trials)
    return total
        



    
    
random.seed(57)

#fix n at 24 and plot binome for a range of weights from .01 to .1
x = np.arange(0.0,1,0.1)
y = [binome(w,24,5000) for w in x]
plt.plot(x,y)
plt.show()

