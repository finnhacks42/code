import shapefile
import shapely
from shapely.geometry import Polygon
from shapely.geometry import Point
from rtree import index
import csv


# load polygons.
sf = shapefile.Reader("/home/finn/phd/data/3rdparty/census_shp/2000/block/tl_2010_48113_tabblock00.shp")
polygon_shapes = sf.shapes()
polygons = [Polygon(q.points) for q in polygon_shapes] # creats polygon objects from lists of points
block_ids = [x[4] for x in sf.records()] # pulls out the block id column from each row of attributes in the shapefile

indx = index.Index() # create an r-tree index for fast lookups (creates a nested hierachy of boxes to check)
for i,q in enumerate(polygon_shapes): 
    indx.insert(i,q.bbox) # add each polygon to the index with the id equal to its row number in the shapefile (and correpondingly the index into block_ids)

# read in the raw data with lat, lon
# TODO think carefully about projection (are the points in the same projection as the shapefile?)
#I can check this by creating a shapefile with a single block in it and seeing which points are supposed to fit in it and mapping them in QGIS

with open('/home/finn/phd/data/geocoded_clean_10.txt', 'rb') as csvfile:
...     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
...     for row in spamreader:
...         print ', '.join(row)
Spam, Spam, Spam, Spam, Spam, Baked Beans
Spam, Lovely Spam, Wonderful Spam

    

