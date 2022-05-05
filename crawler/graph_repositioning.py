import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

#This script takes the output file of extractor.py and makes a plot with the repositioned graph
#Idea: https://stackoverflow.com/questions/55750436/group-nodes-together-in-networkx
graph = nx.read_gml("Graph.gml")
pos = nx.circular_layout(graph)
# prep center points (along circle perimeter) for the clusters
angs = np.linspace(0, 2*np.pi, 6)
repos = []
rad = 5     # radius of circle
for ea in angs:
    if ea > 0:
        repos.append(np.array([rad*np.cos(ea), rad*np.sin(ea)]))

for ea in pos.keys():
    if graph.nodes[ea]['color'] == 'r':
        posx = 0
    elif graph.nodes[ea]['color'] == 'b':
        posx = 1
    elif graph.nodes[ea]['color'] == 'g':
        posx = 2
    elif graph.nodes[ea]['color'] == 'y':
        posx = 3
    elif graph.nodes[ea]['color'] == 'pink':
        posx = 4
    else:
        pass
    pos[ea] += repos[posx]

node_colors = [graph.nodes[v]['color'] for v in graph.nodes]  # list of node colors
nx.draw(graph, pos, with_labels=True, font_weight='normal', node_size=100, font_size=8, node_color = node_colors)
plt.show()
