import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import edgeList

# edgeList extraction
edgeList = edgeList.run()  # receive edge list in format [ [origin_node, target_node] ]
# print(edgeList)

graph = nx.DiGraph()
graph.add_edges_from(edgeList)  # create graph from directed edge list
# graph = nx.DiGraph()
# nx.write_gml(graph, r'Graph_new.gml')  # save graph to file
nx.draw(graph, with_labels=True, font_weight='normal', node_size=100, font_size=8)  # TODO: node colors

# visualization
plt.show()  # TODO: styling of graph
# plt.savefig('first_three_comments.png', dpi=500)

