# creates a suburb network from tweets and a given shapefile
import shapefile
import shapely
from shapely.geometry import Polygon
from shapely.geometry import Point
from rtree import index
import networkx as nx
#TODO remove stuff in brackets from node labels

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
journeys = []
total_length = 0
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
                    journey.append(burb)
                break
    if len(journey) > 1:
        journeys.append(journey)
        total_length+=len(journey)
 
# create a network
G = nx.Graph()
# add nodes
for i in range(len(suburb_names)):
    G.add_node(i,label=suburb_names[i])

# add edges
for j in journeys:
    for n in range(1,len(j)):
        a = j[n-1]
        b = j[n]
        # create a link a-b
        edge_data = G.get_edge_data(a,b)
        if edge_data is None:
            G.add_edge(a,b,weight=1)
        else:
            w = edge_data["weight"]+1
            G.add_edge(a,b,weight=w)


# remove nodes with 0 links.
delete = []
for key,value in G.degree().iteritems():
    if value < 1:
        delete.append(key)
G.remove_nodes_from(delete)
        
nx.write_gml(G,"/home/finn/phd/data/tweets/twitter_graph.gml")          


print "Done"
