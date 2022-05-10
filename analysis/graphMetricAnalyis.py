import networkx as nx
import os

path = os.getcwd()

# Read graph from gml file as G
G = nx.read_gml("../crawler/Graph.gml")

# Adjacency Matrix A
A = nx.adjacency_matrix(G)


# print all metrics of the graph GF that are implemented in this class
def global_properties(GF):
    print('number of nodes: ', nx.number_of_nodes(GF))
    print('number of edges: ', nx.number_of_edges(GF))
    # print('diameter', nx.diameter(GF))
    print('Average clustering coefficient: ', average_clustering_coefficient(G))
    print('Average degree centrality:', average_in_degree(G))  # For directed graph
    print('Average in degree centrality:', average_in_degree(G))  # For directed graph
    print('Average out degree centrality:', average_out_degree(G))  # For directed graph
    print('Average betweenness centrality:',  average_betweennes_centrality(GF))
    print('Graph density: ', nx.density(GF))


# returns a list of nodes that have an in_degree of at least 'limit'
def calculate_in_degree(GF, limit):
    res = []
    nodes = list(GF.nodes())
    for node in nodes:
        indeg = G.in_degree(node)
        if indeg < limit:
            continue
        else:
            res.append((node, indeg))
    return res


# returns a list of nodes that have an out_degree of at least 'limit'
def calculate_out_degree(GF, limit):
    res = []
    nodes = list(GF.nodes())
    for node in nodes:
        outdeg = G.out_degree(node)
        if outdeg < limit:
            continue
        else:
            res.append((node, outdeg))
    return res


# returns a list of nodes that have an degree of at least 'limit'
def calculate_degree(GF, limit):
    res = []
    nodes = list(GF.nodes())
    for node in nodes:
        outdeg = nx.degree(node)
        if outdeg < limit:
            continue
        else:
            res.append((node, outdeg))
    return res


# sorts a list and returns it, if desc=true, it will be sorted descending, otherwise ascending
def sort_list(listToSort, desc):
    listToSort.sort(key=lambda x: x[1], reverse=desc)
    return listToSort


# returns the average in-degree of the graph GF as double
def average_in_degree(GF):
    degree_sum = 0
    degree_list = calculate_in_degree(GF, 0)
    for item in degree_list:
        degree_sum += item[1]
    return degree_sum / nx.number_of_nodes(GF)


# returns the average out-degree of the graph GF as double
def average_out_degree(GF):
    degree_sum = 0
    degree_list = calculate_out_degree(GF, 0)
    for item in degree_list:
        degree_sum += item[1]
    return degree_sum / nx.number_of_nodes(GF)

# returns the average degree of the graph GF as double
def average_degree(GF):
    degree_sum = 0
    degree_list = calculate_degree(GF, 0)
    for item in degree_list:
        degree_sum += item[1]
    return degree_sum / nx.number_of_nodes(GF)


# returns the clustering coefficient of the graph GF as double
def average_clustering_coefficient(GF):
    cc = nx.average_clustering(GF)
    return cc


# returns the average betweenness centrality of the graph GF as double
def average_betweennes_centrality(GF):
    betweenness_sum = 0;
    bc = nx.betweenness_centrality(GF)
    for key, value in bc.items():
        betweenness_sum += value
    return betweenness_sum / nx.number_of_nodes(GF)


print("Graph metrics:")

outdegree = calculate_out_degree(G, 10)
indegree = calculate_in_degree(G, 25)

outdegree = sort_list(outdegree, True)
indegree = sort_list(indegree, True)

print("\n-----Out-degree-----\n")
for node in outdegree:
    print(node)

print("\n-----In-degree-----\n")
for node in indegree:
    print(node)
# centrality_measures(G)
global_properties(G)