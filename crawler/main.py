import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import edgeList

edgeList = edgeList.run()  # receive edge list in format [ [origin_node, target_node] ]
# print(edgeList)
df = pd.DataFrame(edgeList)  # convert edge list to pandas dataframe
# print(df)
graph = nx.from_pandas_edgelist(df, 0, 1)  # create graph from dataframe edge list
# graph = nx.DiGraph()
# nx.write_gml(graph, r'Graph_new.gml')  # save graph to file
nx.draw(graph, with_labels=True, font_weight='bold')  # TODO: node colors
plt.show()  # TODO: styling of graph

