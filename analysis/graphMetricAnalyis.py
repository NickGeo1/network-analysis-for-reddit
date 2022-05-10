import networkx as nx
import os
import matplotlib.pyplot as plt
import collections
import numpy as np
from scipy.optimize import curve_fit
import pandas as pd

path = os.getcwd()

# Read graph from gml file as G
G = nx.read_gml("../crawler/Graph.gml")
G_undirected = nx.Graph(G) #undirected version of the graph for some calculations

# Adjacency Matrix A
A = nx.adjacency_matrix(G)
#print(A.todense())

#Print all metrics of the graph GF that are implemented in this class and are being requested from task 4
#Diameter, average path length are being calculated via Gephi
def global_properties(G, G_undirected):
    remove = remove_nodes(G_undirected, False)
    G_new_undirected = nx.Graph(G_undirected) #undirected graph without nodes that dont have neighbors or have only selfloops
    G_new_undirected.remove_nodes_from(remove)
    #Connected_Graph = G.remove_nodes_from(remove)
    #nx.write_gml(Connected_Graph, r'Connected_Graph.gml') #Export the directed graphs with the removed nodes

    print('number of nodes: ', nx.number_of_nodes(G))
    print('number of edges: ', nx.number_of_edges(G))

    print('Average shortest path length between 2 nodes in the graph calculated by Gephi(undirected version): : 5.40834432276679')

    path_len = dict(nx.all_pairs_shortest_path_length(G_new_undirected))
    list_of_paths_lengths = []
    for dic in path_len.values():
        list_of_paths_lengths += [val for val in dic.values() if val != 0]   
    print('Variance of shortest path lengths between 2 nodes in the graph(undirected version):', np.var(list_of_paths_lengths))

    print('Diameter of the graph(undirected version): ', max(list_of_paths_lengths))
    print('Diameter of the graph(directed version, calculated by Gephi): 23')

    print('Average clustering coefficient(undirected version): ', average_clustering_coefficient(G_undirected))
    print('Average clustering coefficient excluding nodes without neighbours and with only selfloops(undirected version): ', average_clustering_coefficient(G_new_undirected))

    print('Average in degree centrality(undirected version) and its variance:', average_in_degree_and_variance(G_undirected))
    print('Average in degree centrality (excluding nodes without neighbours and with only selfloops, undirected version) and its variance:', average_in_degree_and_variance(G_new_undirected))
   
    print('Average out degree centrality(undirected version):', average_out_degree_and_variance(G_undirected))
    print('Average out degree centrality (excluding nodes without neighbours and with only selfloops, undirected version) and its variance:', average_out_degree_and_variance(G_new_undirected))
    
    print('Average betweenness centrality(undirected version) and its variance:',  average_betweennes_centrality_and_variance(G_undirected))
    print('Average betweenness centrality (excluding nodes without neighbours and with only selfloops, undirected version) and its variance:',  average_betweennes_centrality_and_variance(G_new_undirected))
 
    print('Average closeness centrality(undirected version) and its variance:',  average_closeness_centrality_and_variance(G_undirected))
    print('Average closeness centrality (excluding nodes without neighbours and with only selfloops,undirected version) and its variance:',  average_closeness_centrality_and_variance(G_new_undirected))
   
    giant_component = max(nx.connected_components(G_undirected), key=len)
    giant_component_subgraph = G_undirected.subgraph(giant_component).copy()
    #nx.write_gml(giant_component_subgraph, r'Giant_component_subgraph.gml') #Export the component subgraph 

    #print('The set of nodes of the largest connected component of the graph is(undirected version): ', giant_component)
    print('The size of the largest connected component is: ', len(giant_component))

    #print('Graph density: ', nx.density(GF))


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

# returns the average in-degree and its variance of the graph GF as double
def average_in_degree_and_variance(GF):
    degree_sum = 0
    degree_list = calculate_in_degree(GF, 0)
    for item in degree_list:
        degree_sum += item[1]
    average = degree_sum / nx.number_of_nodes(GF)
    variance = np.var([item[1] for item in degree_list])
    return average, variance


# returns the average out-degree and its variance of the graph GF as double
def average_out_degree_and_variance(GF):
    degree_sum = 0
    degree_list = calculate_out_degree(GF, 0)
    for item in degree_list:
        degree_sum += item[1]
    average = degree_sum / nx.number_of_nodes(GF)
    variance = np.var([item[1] for item in degree_list])
    return average, variance

# returns the average degree of the graph GF as double
def average_degree(GF):
    degree_sum = 0
    degree_list = calculate_degree(GF, 0)
    for item in degree_list:
        degree_sum += item[1]
    return degree_sum / nx.number_of_nodes(GF)


# returns the average clustering coefficient and its variance of the graph GF as double
def average_clustering_coefficient(GF):
    cc = nx.average_clustering(GF)
    return cc

# returns the average betweenness centrality and its variance of the graph GF as double
def average_betweennes_centrality_and_variance(GF):
    betweenness_sum = 0;
    bc = nx.betweenness_centrality(GF)
    for key, value in bc.items():
        betweenness_sum += value
    average = betweenness_sum / nx.number_of_nodes(GF)
    variance = np.var([item for item in bc.values()])
    return average, variance

# returns the average closeness centrality and its variance of the graph GF as double
def average_closeness_centrality_and_variance(GF):
    Clc = nx.closeness_centrality(GF)
    return sum(Clc.values())/len(Clc.values()), np.var([item for item in Clc.values()])

def print_top_n_degree_stats(GF, n):
    outdegree = calculate_out_degree(GF, n)
    indegree = calculate_in_degree(GF, n)

    outdegree = sort_list(outdegree, True)
    indegree = sort_list(indegree, True)

    print("\n-----Out-degree-----\n")
    #for node in outdegree:
        #print(node)


    print("\n-----In-degree-----\n")
    for node in indegree:
        print(node)

#returns a list with nodes without neighbours and with only selfloops
def remove_nodes(G, directed):
    new_G = nx.Graph(G) if directed else G #make the graph undirected 
    nodes_to_remove = [] #list for nodes to remove
    for node in new_G:
        if new_G[node] == {} or list(new_G[node].keys()) == [node]: #if node has not neighbors or only a selfloop
            nodes_to_remove.append(node)
    return nodes_to_remove

def func(x, a, b):
    return a * (x ** -b)

# returns a plot that shows the distribution of the list from paramameter
# degree_list needs to have lists as items, whereas the second item is relevant for plotting
# in logartihmic scale: log = True
def is_power_law(GF, degree_list, log):
    dist = {}
    for item in degree_list:
        degree = item[1]
        if degree in dist:
            dist[degree] += 1
        else:
            dist[degree] = 1
    dist = collections.OrderedDict(sorted(dist.items()))
    xdata, ydata = zip(*dist.items())
    ydata = list(map(lambda x: x / nx.number_of_nodes(GF), ydata))

    #popt, pcov = curve_fit(func, xdata, ydata)
    #plt.plot(xdata, func(xdata, *popt))
    plt.plot(xdata, ydata)
    plt.xlabel("Degree")
    plt.ylabel("Rel. Occurence")
    if log:
        plt.yscale("log")
        plt.xscale("log")
    plt.show()
    # scipy.optimize.curve_fit function with custom power_law function
    # nx.powerlaw_cluster_graph(n, m p)


# print("Graph metrics:")
# centrality_measures(G)
# global_properties(G)
# print_top_n_degree_stats(G, 10)

#is_power_law(G, calculate_in_degree(G, 0), False)
global_properties(G, G_undirected)
