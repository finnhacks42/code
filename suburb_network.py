# creates a suburb network from tweets and a given shapefile
import shapefile
import shapely
from shapely.geometry import Polygon
from shapely.geometry import Point
from rtree import index

# loads all the polygons
sf = shapefile.Reader("/home/finn/phd/data/3rdparty/NSW/1270055003_ssc_2011_aust_shape/Sydney_suburbs.shp")
polygon_shapes = sf.shapes()
polygons = [Polygon(q.points) for q in polygon_shapes]
suburb_names = [x[1] for x in sf.records()]

indx = index.Index()
count = 0
for q in polygon_shapes:
    indx.insert(count,q.bbox)
    count +=1

# load all the journeys
f = open("/home/finn/phd/data/tweets/journeys.csv","r")
for line in f.readlines():
    line = line.split(":")
    journey = []
    last_suburb = None
    for point in line:
        coords = point.split(",")
        p = Point(float(coords[0]),float(coords[1]))
        # figure out which bounding boxes this point fits in
        possible_burbs = indx.intersection((p.x,p.y))
        for burb in possible_burbs:
            if p.within(polygons[burb]):
                if burb != last_suburb:
                    last_suburb = burb
                    journey.append(suburb_names[burb])
                break
    print journey
            
            
        # get the suburb
        # it would be nice to get the names of the suburb out
#f.close()

print "Done"
