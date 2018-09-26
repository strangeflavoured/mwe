import networkx as nx
import matplotlib.pyplot as plt

nodes=['A','B','C','D']
edges=[('A','B'),('A','D'),('D','B'),('C','D')]

G=nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

fig,ax=plt.subplots(1,1)
nx.draw_networkx(G, pos=nx.kamada_kawai_layout(G))
plt.show()