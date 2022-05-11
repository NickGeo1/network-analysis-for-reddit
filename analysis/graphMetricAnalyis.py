import networkx as nx
import os
import matplotlib.pyplot as plt
import collections
import numpy as np
from scipy.optimize import curve_fit

path = os.getcwd()

# Read graph from gml file as G
G = nx.read_gml("../crawler/Graph.gml")

# Adjacency Matrix A
A = nx.adjacency_matrix(G)


# print all metrics of the graph GF that are implemented in this class
def global_properties(GF):
    print('number of nodes: ', nx.number_of_nodes(GF))
    print('number of edges: ', nx.number_of_edges(GF))
    # print('diameter', nx.diameter(nx.to_undirected(GF)))
    print('Average clustering coefficient: ', average_clustering_coefficient(G))
    print('Average clustering coefficient: ', nx.average_clustering(G))
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
        deg = nx.degree(GF, node)
        if deg < limit:
            continue
        else:
            res.append((node, deg))
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


def print_top_n_degree_stats(GF, n):
    outdegree = calculate_out_degree(GF, n)
    indegree = calculate_in_degree(GF, n)
    degree = calculate_degree(GF, n)

    outdegree = sort_list(outdegree, True)
    indegree = sort_list(indegree, True)
    degree = sort_list(degree, True)

    print("\n-----Out-degree-----\n")
    for node in outdegree:
        print(node)

    print("\n-----In-degree-----\n")
    for node in indegree:
        print(node)

    print("\n-----Degree-----\n")
    for node in degree:
        print(node)


def func(x, a, b):
    return a * (x ** b)
    # return (a * x) + b
    #return a * np.exp(-b ** x)


# returns a plot that shows the distribution of the list from paramameter
# degree_list needs to have lists as items, whereas the second item is relevant for plotting
# in logartihmic scale: log = True
def is_power_law(GF, degree_list, log):
    dist = {}
    for item in degree_list:
        degree = item[1]
        #if degree % 2 != 0:
        #    continue
        #if degree > 20:
        #    continue
        if degree in dist:
            dist[degree] += 1
        else:
            dist[degree] = 1
    dist = collections.OrderedDict(sorted(dist.items()))

    #for key, value in dist.items():
    #    print("degree: ", key, ", count: ", value, "; fraction: ", value / nx.number_of_nodes(GF))
    xdata, ydata = zip(*dist.items())
    ydata = list(map(lambda x: x / nx.number_of_nodes(GF), ydata))
    xdata = list(map(lambda x: float(x), xdata))

    popt, pcov = curve_fit(func, xdata, ydata)
    ydata_new = list(map(lambda x: func(x, *popt), xdata))
    print(popt)
    plt.plot(xdata, ydata_new, 'r-',  label='fit: a=%5.3f, b=%5.3f' % tuple(popt))
    plt.plot(xdata, ydata, label='data')
    plt.xlabel("Degree")
    plt.ylabel("Fraction of users")
    if log:
        plt.yscale("log")
        plt.xscale("log")
    plt.legend()
    plt.show()


# global_properties(G)
# print_top_n_degree_stats(G, 10)
is_power_law(G, calculate_out_degree(G, 1), True)
