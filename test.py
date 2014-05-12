import networkx as nx

G = nx.Graph()

for i in range(10):
    for j in range(10):
        G.add_edge(i,j,weight=1)

print G.size()
print G.get_edge_data(0,1)
print G.get_edge_data(12,13)
