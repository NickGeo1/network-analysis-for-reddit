import matplotlib  
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import networkx as nx
from datetime import date
import datetime
import os
import sys
cwd = os.getcwd()
path = cwd+"/../analysis"
sys.path.insert(0, path)
from graphMetricAnalyis import is_power_law
       
graph = nx.read_gml("Graph.gml")
#Dates of creation of each of the top5 posts (starting from top1)
top_5_posts_created = ['2022-04-27 17:33:35', '2022-04-30 17:21:55', '2022-04-05 05:08:51', '2022-04-20 16:42:23', '2022-05-01 19:54:34']
submission_colors = ["r","b","g","y","pink"]
#We create a list with all the comment dates sorted from older to newer
all_dates_list = []
for v in graph.nodes:
    all_dates_list += [date for date in graph.nodes[v]['created']]
all_dates_list.sort()

#We create a list of groups, each group including a post's comment dates in sorted order
date_groups = []
for color in submission_colors:
    group = []
    for v in graph.nodes:
        if graph.nodes[v]['color'] == color:
            group += [d for d in graph.nodes[v]['created']]
    group.sort()
    date_groups.append(group)

def plot_comments_per_day(post_created_at, comment_date_list, title, color):
    post_created_at = post_created_at.split(" ")[0] #take the date part of the string
    comment_date_list = [date.split(" ")[0] for date in comment_date_list] #We take only the date parts from the sorted date list

    first_y_m_d = post_created_at.split("-")
    first_y_m_d = [int(element) for element in first_y_m_d] #Take the y,m,d of first ploting date as ints in a list

    last_y_m_d = comment_date_list[-1].split("-")
    last_y_m_d = [int(element) for element in last_y_m_d] #Take the y,m,d of last ploting date as ints in a list

    first_day, last_day = date(*first_y_m_d), date(*last_y_m_d) #Get the first and last day objects

    plot_days_count = (last_day - first_day).days #How many days to plot
    plot_days = np.array([str(first_day + datetime.timedelta(days=d)) for d in range(plot_days_count+1)]) #Get an array with all the plot days

    comments_count = [comment_date_list.count(d) for d in plot_days] #Get the ammount of comments in each day

    #Make 3 plots in the same window

    #Bar plot representing comments per day
    fig = plt.figure(constrained_layout=True)
    gs = GridSpec(8, 8, figure=fig)
    fig.add_subplot(gs[:4, :4])
    plt.bar(plot_days, comments_count, color = color)    
    for i in range(len(plot_days)):
        plt.text(i, comments_count[i]//2, comments_count[i], ha = 'center', fontweight = 'bold', fontsize = 8)
    plt.title(title, fontsize=14, fontweight = 'bold', color = color)
    plt.xlabel('Days', fontsize=14, fontweight = 'bold')
    plt.ylabel('Comments', fontsize=14, fontweight = 'bold')
    plt.xticks(rotation = 90, fontsize = 8)
    plt.grid(True)

    #Function plot representing comments per day
    dates_counts = (plot_days, comments_count)
    fig.add_subplot(gs[:4, 4:])
    is_power_law(None, dates_counts, False, title, 'Days', 'Comments', color, False)

    #Function plot representing comments per day in log scale(trying to check if power law fits)
    fig.add_subplot(gs[4:, 2:6])
    is_power_law(None, dates_counts, True, title+" LOG SCALE", 'Days', 'Comments', color, False)

#Here, we use this function to run the plot for the whole data.
plot_comments_per_day(min(top_5_posts_created), all_dates_list, "TOTAL COMMENTS PER DAY FOR TOP 5 POSTS", 'orange')
#Here, we use this function to run the plot for every group of data.
for post_date, date_list, i, color in zip(top_5_posts_created, date_groups, list(range(len(top_5_posts_created))), submission_colors):
    plot_comments_per_day(post_date, date_list, f"COMMENTS PER DAY FOR TOP {i+1} POST", color)
plt.show()
