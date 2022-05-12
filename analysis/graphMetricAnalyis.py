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
G_undirected = nx.Graph(G)  # undirected version of the graph for some calculations

# Adjacency Matrix A
# A = nx.adjacency_matrix(G)
# print(A.todense())


# Print all metrics of the graph GF that are implemented in this class and are being requested from task 4
# Diameter, average path length are being calculated via Gephi
def global_properties(G, G_undirected):
    remove = remove_nodes(G_undirected, False)
    G_new_undirected = nx.Graph(G_undirected)  # undirected graph without nodes that dont have neighbors or have only selfloops
    G_new_undirected.remove_nodes_from(remove)
    # Connected_Graph = G.remove_nodes_from(remove)
    # nx.write_gml(Connected_Graph, r'Connected_Graph.gml') #Export the directed graphs with the removed nodes

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


# returns a list of tuples, each tuple containing the node and the in-degree of at least 'limit'
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


# returns a list of tuples, each tuple containing the node and the out-degree of at least 'limit'
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


# returns a list of tuples, each tuple containing the node and the degree of at least 'limit'
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


# returns a list with nodes without neighbours and with only selfloops
def remove_nodes(G, directed):
    new_G = nx.Graph(G) if directed else G #make the graph undirected 
    nodes_to_remove = [] #list for nodes to remove
    for node in new_G:
        if new_G[node] == {} or list(new_G[node].keys()) == [node]: #if node has not neighbors or only a selfloop
            nodes_to_remove.append(node)
    return nodes_to_remove


def func(x, a, b):
    return a * (x ** (-b))
    # return (a * x) + b
    #return a * np.exp(-b ** x)

# returns the age of popularity of one user. Practicaly this is how many days that user
# got replies since the first day he made the comment
#def calculate_comment_age(G, user_node):


# shows a plot that shows the distribution of the list from paramameter
# data_list is either: 
# -a list of tuples, each tuple containing the name of a user and his in/out degree
# -a tuple with two lists, where the first list contains dates and the second list how many comments made at the corresponding date of first list
# in logartihmic scale: log = True
def is_power_law(GF, data_list, log, title, xlabel, ylabel, color, plot = True):

    #If we want the degree distribution, we are making a dictionary with the degrees as keys 
    #and how many nodes with that degree as values
    if xlabel.endswith('Degree'): 
        dist = {}
        for item in data_list:
            degree = item[1]
            #if degree % 2 != 0:
            #    continue
            #if degree > 20:
            #    continue
            if degree in dist:
                dist[degree] += 1
            else:
                dist[degree] = 1
        dist = collections.OrderedDict(sorted(dist.items())) #sort the dictionary

        #for key, value in dist.items():
        #    print("degree: ", key, ", count: ", value, "; fraction: ", value / nx.number_of_nodes(GF))
        xdata, ydata = zip(*dist.items())  #xdata = list of degrees, ydata = list of how many nodes with that degree
    
        xdata = list(map(lambda x: float(x), xdata)) #make xdata floats
        ydata = list(map(lambda x: x / nx.number_of_nodes(GF), ydata)) #normalize the amount of nodes with degreee k in [0,1]
        popt, pcov = curve_fit(func, xdata, ydata) #Find a,b such that we can fit a function to our data popt=(a,b)
        ydata_new = list(map(lambda x: func(x, *popt), xdata)) #Calculate the y of the above found function

    #In this case we want to plot comments per day. Our x data now is dates, so in order
    #to find a function that fits our data function, we have to consider these dates as numbers. In linear scale, dates
    #are 1,2,3,4,...,len(xdata) and in log scale 1,10,100,...,10^(len(xdata)-1)
    else:
        xdata, ydata = data_list[0], data_list[1]
        if log:
            #We have to check and remove if some dates have 0 comments. These y values mess up our
            #log scale plot
            x_y_to_remove = []
            x_y = list(zip(xdata, ydata))
            for xy in x_y:
                if xy[1] == 0:
                    x_y_to_remove.append(xy)
            for xy in x_y_to_remove:
                x_y.remove(xy)
            xdata, ydata = zip(*x_y)
            #these numbers are going to override the dates in order to find the fit function (log scale)
            xdata_nums = [10**x for x in range(len(xdata))]
        else:
            #these numbers are going to override the dates in order to find the fit function
            xdata_nums = [x+1 for x in range(len(xdata))]
        popt, pcov = curve_fit(func, xdata_nums, ydata)
        ydata_new = list(map(lambda x: func(x, *popt), xdata_nums))
        plt.xticks(rotation = 90, fontsize = 8) #rotate date labels by 90 degrees
    
    print(popt)
    plt.title(title, fontsize=14, fontweight = 'bold', color = color)

    #If we want to plot log scale of comments per day, we make a plot
    #with x values from 1 through 10^(len(xdata)-1) and then we replace
    #each 10^n value with the dates
    if log and xlabel == "Days":
        plt.yscale("log")
        plt.xscale("log")
        plt.plot([float(10**x) for x in range(len(xdata))], ydata, color, label='data') #data
        plt.plot([float(10**x) for x in range(len(xdata))], ydata_new, 'k-',  label='fit: a=%5.3f, b=%5.3f' % tuple(popt)) #function that fits best
        plt.xticks([float(10**x) for x in range(len(xdata))], xdata) #replace numbers with labels
    #If we want to plot log scale of degree distribution, we just plot the x and
    #the corresponding y data where x is a list of degrees and y the corresponding fraction of
    #users with that degree
    elif log and xlabel.endswith('Degree'):
        plt.yscale("log")
        plt.xscale("log")
        plt.plot(xdata, ydata, color, label='data')
        plt.plot(xdata, ydata_new, 'k-',  label='fit: a=%5.3f, b=%5.3f' % tuple(popt))
    #In case of linear scale: 
    #-dates in xdata fit with the corresponding comments in ydata
    #-degrees in xdata fit with the corresponding user fractions in ydata
    elif not log:
        plt.plot(xdata, ydata, color, label='data')
        plt.plot(xdata, ydata_new, 'k-',  label='fit: a=%5.3f, b=%5.3f' % tuple(popt))

    plt.xlabel(xlabel, fontsize=14, fontweight = 'bold')
    plt.ylabel(ylabel, fontsize=14, fontweight = 'bold')       
    plt.legend()

    if plot:
        plt.show()


# global_properties(G)
# print_top_n_degree_stats(G, 10)

if __name__ == "__main__":
    is_power_law(G, calculate_in_degree(G, 0), False, "In degree centrality distribution", "In Degree", "Fraction of users", "b")
    is_power_law(G, calculate_in_degree(G, 0), True, "In degree centrality distribution", "In Degree", "Fraction of users","b")
    is_power_law(G, calculate_out_degree(G, 0), False, "Out degree centrality distribution", "Out Degree", "Fraction of users","b")
    is_power_law(G, calculate_out_degree(G, 0), True, "Out degree centrality distribution", "Out Degree", "Fraction of users","b")

#global_properties(G, G_undirected)
