# creates a suburb network from tweets and a given shapefile
import shapefile
import shapely
from shapely.geometry import Polygon
import pyproj
import osgeo

# loads all the polygons
#polygons_sf = shapefile.Reader("/home/finn/phd/data/3rdparty/NSW/1270055003_ssc_2011_aust_shape/Sydney_suburbs2.shp")
#polygon_shapes = polygons_sf.shapes()
#polygons = [Polygon(q.points) for q in polygon_shapes]

# load all the points (ie the journeys) - I want a convinient output format to store geospatial data

print "Done"
