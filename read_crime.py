import csv
import networkx as nx



path = "/home/finn/phd/data/"

class BiGraph:
    def __init__(self):
        self.G = nx.Graph()
        self.edges = {}
    def add(self,source,dest):
        self.G.add_node(source,category="0")
        self.G.add_node(dest,category = "1")
        w = self.edges.get((source,dest),0)
        w +=1
        self.edges[(source,dest)] = w
    def getGraph(self):
        for edge_tuple,w in self.edges.iteritems():
            self.G.add_edge(edge_tuple[0],edge_tuple[1],weight=w)
        return self.G
        
with open(path+"geocoded_clean.txt","r") as f, open(path+"cop_ra.gml","w") as graph_file:
    r = csv.reader(f,delimiter="\t",quotechar='"')
    header = r.next()
    cols = len(header)
    header = dict(zip(header,range(cols)))
    graph = BiGraph()
    rows = 0
    for line in r:
        rows +=-1
        if rows > 1000:
            break
        officer = "O"+line[header["reporting_officer_badge1"]].replace(" ","")
        area = "A"+line[header["reportingarea"]].replace("_","").replace(" ","")
        graph.add(officer,area)

    G = graph.getGraph()
    nx.write_gml(G,graph_file)
    nx.write_graphml(G,path+"cop_ra.graphml")
    nx.write_gexf(G,path+"cop_ra.gexf")
    print "Nodes,",G.number_of_nodes()
    print "Edges,",G.number_of_edges()
    
    
        
        
                    
                    
    
