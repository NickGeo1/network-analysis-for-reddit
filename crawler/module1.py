import praw
import networkx as nx
import matplotlib.pyplot as plt
import time
from datetime import datetime

# use praw.ini file to initialize reddit object
reddit = praw.Reddit("bot1", user_agent="bot1 user agent")

# testing that it is the correct user
print(f"current user: {reddit.user.me()}")

# reddit post urls
urls = [("https://www.reddit.com/r/wallstreetbets/comments/u7wtfh/5k_to_100k_overnight_nflx_put/?utm_source=share" \
      "&utm_medium=web2x&context=3 ","red")
        ]

graph = nx.DiGraph()

#We return a list with the edges that form a tree-interaction graph between users starting from
#a single lv0 comment
def make_tree(comment):
    single_comment_edges = []
    edge_nodes = []
    for reply in comment.replies:  # every 2nd level reply is child of comment
        if reply.author is None:  # If comment is deleted author = none
            continue
        comment_created = datetime.fromtimestamp(comment.created_utc)
        reply_created = datetime.fromtimestamp(reply.created_utc)
        single_comment_edges += [(reply.author.name, comment.author.name)]
        edge_nodes += [(reply.author.name, [reply_created]), (comment.author.name, [comment_created])]
        edges, nodes = make_tree(reply)
        single_comment_edges += edges
        edge_nodes += nodes

    return single_comment_edges, edge_nodes

#We return a list of node-users without replies and a list of edges that represent the graph of users
#that interact with each other by replies, given a post
def make_forest(post):
    graph_edges = []
    graph_nodes = []
    post.comments.replace_more(limit=None)  # replace all MoreComments objects with the actual comments
    for comment in post.comments[:2]:
        if comment.author is None:  # If comment is deleted author = none
            continue
        if len(comment.replies) == 0:
            comment_created = datetime.fromtimestamp(comment.created_utc)
            graph_nodes.append((comment.author.name, comment_created))
        else:
            edges, nodes = make_tree(comment)
            graph_edges += edges
            graph_nodes += nodes

    return graph_edges, graph_nodes

before = time.time()

for url,color in urls:
    submission = reddit.submission(url=url)
    graph_edges, graph_nodes = make_forest(submission)
    for v,d in graph_nodes:
        if v in graph.nodes and d[0] not in graph.nodes[v]['created']:
            graph.nodes[v]['created'].append(d[0])
        else:
            graph.add_node(v,created=d,color=color)
    graph.add_edges_from(graph_edges)

node_colors = [graph.nodes[v]['color'] for v in graph.nodes]  # list of node colors
nx.draw(graph, with_labels=True, font_weight='normal', node_size=100, font_size=8, node_color = node_colors)  # TODO: node colors
print(f"time: {time.time() - before}")
# visualization
plt.show()  # TODO: styling of graph
# plt.savefig('first_three_comments.png', dpi=500)
print(graph.nodes.data())