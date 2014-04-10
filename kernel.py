from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import math

def readData(filename):
    f = open(filename,"r")
    lat = []
    lon = []
    failed = 0
    while True:
        line = f.readline()
        if not line:
            break
        line = line.split("\t")
        try:
            x = float(line[0])
            y = float(line[1])
            lon.append(x)
            lat.append(y)
        except ValueError:
            failed +=1
    f.close()
    if failed > 0:
        print "Warning,",failed,"lines failed to parse"
    return (lon,lat)


def distance(lat1, lon1, lat2, lon2):
    dlat = math.radians(lat1 - lat2)
    dlon = math.radians(lon1 - lon2)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    a = pow(math.sin(dlat/2),2)+pow(math.sin(dlon/2),2)*math.cos(lat1)*math.sin(lat2)
    c  = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    d = 6371000*c
    return d

# data is a tuple containing the longs and lats
# returns a list of length num_folds, each containing a tuple
def make_folds(num_folds, data):
    events = len(data[0])
    fold_size = int(events/float(num_folds))
    result = []
    s_indx  = 0
    e_indx = fold_size
    for i in range(num_folds):
        if e_indx > events:
            e_indx = events
        lon = data[0][s_indx:e_indx]
        lat = data[1][s_indx:e_indx]
        result.append((lon,lat))
        s_indx += fold_size
        e_indx += fold_size
    return result

# folds is a list of tuples of lat lons, returns a single tuple of lat longs
def combine_folds(folds):
    lon = []
    lat = []
    for f in folds:
        lon.extend(f[0])
        lat.extend(f[1])
    return (lon,lat)

def cost(kernel, test):
    return 1

def kde(folds, fold_number, bw):
    test = folds[fold_number]
    train = folds[0:fold_number]
    if fold_number < len(folds) - 1:
        train.extend(folds[fold_number+1:])
    # join the values together so that there is one row for x-coordinates and one for y-coordinates
    values = np.vstack(train)
    kernel = stats.gaussian_kde(values, bw)
    # calculate the cost
    c = cost(kernel,test)
    return (kernel,cost)                

def make_grid(lon,lat):
    xmin = min(lon)
    xmax = max(lon)
    ymin = min(lat)
    ymax = max(lat)
    print "height",distance(xmin,ymin,xmin,ymax)
    print "width",distance(xmin,ymin,xmax,ymin)
    # creates a pair of 100x100 arrays. The first contains the x-coordinates in the grid, the 2nd - the y-coordinates
    X,Y = np.mgrid[xmin:xmax:100j,ymin:ymax:100j]
    # reshapes the data to create a single array, with the 1st row the x-coordinates and the 2nd row the y-coordinates (ravel flatterns an array)
    # each row is 10000 long (100x100)
    positions = np.vstack([X.ravel(), Y.ravel()])
    return positions,X.shape,[xmin,xmax,ymin,ymax]

def do_plot(kernel,grid_array,shape,bounds):
    Z = np.reshape(kernel(grid_array).T, shape)
    # plot the data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(np.rot90(Z), cmap=plt.cm.gist_earth_r,extent=bounds)
    #ax.plot(lon, lat, 'k.', markersize=2)
    ax.set_xlim([bounds[0], bounds[1]])
    ax.set_ylim([bounds[2], bounds[3]])
    plt.show()
    
        
lon,lat = readData("lonlat.csv")
values = np.vstack((lon,lat))
k1 = stats.gaussian_kde(values,0.01)

grid,shape,bounds = make_grid(lon,lat)
do_plot(k1,grid,shape,bounds)


# want to do 10 fold cross-validation to identify the optimal bandwidth
#folds = make_folds(10,(lon,lat))
#for fold in range(10):
#    print "fold",fold
#    kernel = kde(folds,fold,0.001)




# calculate the smoothed value at each of the postions, - an array of 10000 elements
#smoothed = kernel(positions)

# reshape the data back to a 100x100 matrix
#Z = np.reshape(kernel(positions).T, X.shape)


