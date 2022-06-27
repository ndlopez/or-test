"""
Traveling salesman problem using networkx
the best route of the traveller is: 
[0, 3, 4, 19, 12, 2, 7, 10, 18, 5, 13, 6, 11, 9, 15, 14, 8, 16, 17, 1, 0]
"""
import matplotlib.pyplot as plt
import networkx as nx
import networkx.algorithms.approximation as nx_app
import math

G = nx.random_geometric_graph(20,radius=0.4,seed=3)
pos = nx.get_node_attributes(G,"pos")

#depot should be at (0,0)
H = G.copy()

#calc the distances between the nodes as edges weight
for i in range(len(pos)):
    for j in range(i+1,len(pos)):
        dist = math.hypot(pos[i][0]-pos[j][0],pos[i][1]-pos[j][1])
        dist = dist
        G.add_edge(i,j,weight=dist)

cycle = nx_app.christofides(G,weight="weight")
edge_list = list(nx.utils.pairwise(cycle))

#draw closest edges on each node only
nx.draw_networkx_edges(H,pos,edge_color="blue",width=0.5)

#draw route
nx.draw_networkx(G,pos,with_labels=True,edgelist=edge_list,edge_color="red",node_size=200,width=3,)

print("the best route of the traveller is:",cycle)
plt.show()

