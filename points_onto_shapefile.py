import shapefile
import shapely
from shapely.geometry import Polygon
from shapely.geometry import Point
from rtree import index
import csv
import random



# load polygons.

# read in the raw data with lat, lon
# TODO think carefully about projection (are the points in the same projection as the shapefile?)
#I can check this by creating a shapefile with a single block in it and seeing which points are supposed to fit in it and mapping them in QGIS


def geocode(point, rtree_indx,polygons,spatialIDs):
    r = rtree_indx.intersection((point.x,point.y)) #check in the (fast) rtree which polygons the point might fall into
    for rID in r:
        if point.within(polygons[rID]):
            return block_ids[rID]


def findSpatialID(key,point,rtree_indx,polygons,spatialIDs,key_boundary_map):
    sid = geocode(point,rtree_indx,polygons,spatialIDs)
    if sid:
        return sid
    sid = key_boundary_map.get(key) # if we have created a shifted point for this address, use the same boundary
    if sid:
        return sid
    else: # its not within any of the polygons - this may be because it lies exactly on a boundary.
        dx = random.uniform(-1,1)*10E-4
        dy = random.uniform(-1,1)*10E-4
        point2 = Point(point.x+dx,point.y+dy)
        sid = geocode(point2,rtree_indx,polygons,spatialIDs)
        key_boundary_map[key]=sid 
        return sid
    
    
    

LAT = "lat"
LON = "lon"
KEY = "key"
WANTED = ["crime_trunk","prem","day"]
INDEX_OF_REGION_IDENTIFIER = 3 # 3 for tracts file 4 for blocks file ...

sf = shapefile.Reader("/home/finn/phd/data/3rdparty/census_shp/2000/tract/dallas_tracts.shp")
polygon_shapes = sf.shapes()
polygons = [Polygon(q.points) for q in polygon_shapes] # creats polygon objects from lists of points

block_ids = [x[INDEX_OF_REGION_IDENTIFIER] for x in sf.records()] # pulls out the block id column from each row of attributes in the shapefile

rtree_indx = index.Index() # create an r-tree index for fast lookups (creates a nested hierachy of boxes to check)
for i,q in enumerate(polygon_shapes):
    rtree_indx.insert(i,q.bbox) # add each polygon to the index with the id equal to its row number in the shapefile (and correpondingly the index into block_ids)

outname = "/home/finn/phd/data/geocoded_tract.csv"
outside = "/home/finn/phd/data/geocoded_outside_tract.csv"
key_boundary = {}
with open('/home/finn/phd/data/geocoded_clean.txt', 'r') as csvfile, open(outname,"w") as out, open(outside,"w") as not_dallas:
    r = csv.reader(csvfile,delimiter="\t",quotechar='"')
    header = r.next()
    # parse the header
    latIndx = header.index(LAT)
    lonIndx = header.index(LON)
    otherIndx = [header.index(x) for x in WANTED]
    keyIndx = header.index(KEY)
    not_matched = 0
    total = 0
    header = ["lon","lat","area"]
    header.extend(WANTED)
    out.write(",".join(header)+"\n")
    for row in r:
        total +=1
        lat = float(row[latIndx])
        lon = float(row[lonIndx])
        key = row[keyIndx]
        p = Point(lon,lat)
        spatialID = findSpatialID(key,p,rtree_indx,polygons,block_ids,key_boundary)
        if spatialID:
            output = [str(lon),str(lat),str(spatialID)]
            output.extend([str(row[i]) for i in otherIndx])
            out.write(",".join(output)+"\n")
        else:
            not_matched +=1
            output = [str(lon),str(lat),"0"]
            output.extend([str(row[i]) for i in otherIndx])
            not_dallas.write(",".join(output)+"\n")
            

print "{} not matched from a total of {}".format(not_matched,total)
print len(key_boundary)
        

