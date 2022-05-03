import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import edgeList

# edgeList extraction
edgeList = edgeList.run()  # receive edge list in format [ [origin_node, target_node] ]
# print(edgeList)

# dataframe creation
df = pd.DataFrame(edgeList)  # convert edge list to pandas dataframe
df = df.rename(columns={0: "source", 1: "target"})
print(df.head(100))

# graph generation
graph = nx.from_pandas_edgelist(df, "source", "target")  # create graph from dataframe edge list
# graph = nx.DiGraph()
# nx.write_gml(graph, r'Graph_new.gml')  # save graph to file
nx.draw(graph, with_labels=True, font_weight='normal', node_size=100, font_size=8)  # TODO: node colors

# visualization
plt.show()  # TODO: styling of graph
# plt.savefig('first_three_comments.png', dpi=500)

