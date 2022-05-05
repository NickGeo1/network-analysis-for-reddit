import praw
import networkx as nx
import matplotlib.pyplot as plt
import time
from datetime import datetime

# use praw.ini file to initialize reddit object
reddit = praw.Reddit("bot1", user_agent="bot1 user agent")

# testing that it is the correct user
print(f"current user: {reddit.user.me()}")

# Top 1 Growing community (subreddit) at 24/4/2022: wallstreetbets
# reddit post colors
submission_colors = ["r","b","g","y","pink"]

graph = nx.DiGraph()

#We return a list with the edges and a list with the child nodes that form a tree-interaction graph between users starting from
#a single lv0 comment
def make_tree(comment):
    single_comment_edges = []
    edge_nodes = []
    for reply in comment.replies:  # every 2nd level reply is child of comment
        if reply.author is None:  # If comment is deleted author = none
            continue
        reply_created = str(datetime.fromtimestamp(reply.created_utc)) 
        single_comment_edges += [(reply.author.name, comment.author.name)]
        edge_nodes += [(reply.author.name, [reply_created])]
        edges, nodes = make_tree(reply)
        single_comment_edges += edges
        edge_nodes += nodes

    return single_comment_edges, edge_nodes

#We return a list of node-users and a list of edges that represent the graph of users
#that interact with each other by replies, given a post
def make_forest(post):
    graph_edges = []
    graph_nodes = []
    post.comments.replace_more(limit=None)  # replace all MoreComments objects with the actual comments
    limit = min(3000, len(post.comments)) #We collect all the subcomments of the first at most 3000 level 0 comments
    for comment in post.comments[:limit]:
        if comment.author is None:  # If comment is deleted author = none
            continue
        comment_created = str(datetime.fromtimestamp(comment.created_utc))
        graph_nodes.append((comment.author.name, [comment_created]))      
        edges, nodes = make_tree(comment)
        graph_edges += edges
        graph_nodes += nodes

    return graph_edges, graph_nodes

before = time.time()

#We get the comments for the first 5 top posts of last month.
for submission, color in zip(list(reddit.subreddit("wallstreetbets").top("month"))[:5], submission_colors):
    #Note that in graph_nodes list we can have duplicate usernames in case one user made more than 1 comment.
    #We keep in mind to store all the dates of all the comments a single user made
    graph_edges, graph_nodes = make_forest(submission)
    for v,d in graph_nodes:
        #if node v is already in graph but the date d of comment that v represents is not included as an attribute
        if v in graph.nodes and d[0] not in graph.nodes[v]['created']: 
            graph.nodes[v]['created'].append(d[0])
        #if node v is not included in graph
        else:
            graph.add_node(v,created=d,color=color)
    for v,u in graph_edges:
        #If an edge added more than one time, we increase the weight by 1 for each duplicate
        if (v,u) in graph.edges:
            graph[v][u]['weight'] += 1
        #If edge is not already included, set weight = 1
        else:
            graph.add_edge(v,u,weight=1)

node_colors = [graph.nodes[v]['color'] for v in graph.nodes]  # list of node colors

#nx.write_gml(graph, r'Graph.gml')  # Save the graph in a file
nx.draw(graph, pos, with_labels=True, font_weight='normal', node_size=100, font_size=8, node_color = node_colors)
print(f"time: {time.time() - before}")
# visualization
plt.show() 
# plt.savefig('first_three_comments.png', dpi=500)