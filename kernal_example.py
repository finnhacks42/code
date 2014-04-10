from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

def measure(n):
    m1 = np.random.normal(size=n) # creates an array of 2000 values
    m2 = np.random.normal(scale=0.5,size=n)
    return m1+m2, m1-m2

m1,m2 = measure(2000)
xmin = m1.min()
xmax = m1.max()
ymin = m2.min()
ymax = m2.max()

# creates a pair of 100x100 arrays. The first contains the x-coordinates in the grid, the 2nd - the y-coordinates
X,Y = np.mgrid[xmin:xmax:100j,ymin:ymax:100j]

# reshapes the data to create a single array, with the 1st row the x-coordinates and the 2nd row the y-coordinates (ravel flatterns an array)
# each row is 10000 long (100x100)
positions = np.vstack([X.ravel(), Y.ravel()])

# join the values together so that there is one row for x-coordinates and one for y-coordinates
values = np.vstack([m1, m2])

# do kernal density estimation, returns a callable that can be used to estimate the dinsity on any points
kernel = stats.gaussian_kde(values)

# calculate the smoothed value at each of the postions, - an array of 10000 elements
smoothed = kernel(positions)

# reshape the data back to a 100x100 matrix
Z = np.reshape(kernel(positions).T, X.shape)

# plot the data
fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(np.rot90(Z), cmap=plt.cm.gist_earth_r,extent=[xmin, xmax, ymin, ymax])
ax.plot(m1, m2, 'k.', markersize=2)
ax.set_xlim([xmin, xmax])
ax.set_ylim([ymin, ymax])
plt.show()
