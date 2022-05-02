import pandas as pd
import praw
from praw.models import MoreComments
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt

#use praw.ini file to initialize reddit object
#reddit = praw.Reddit("bot1", user_agent="bot1 user agent")
reddit = praw.Reddit(
    client_id="_Z-UctTbLwJV10tOmCuMng",
    client_secret="-pvmI9ANIJxLXUA8Ue3t_Hq2GvvlUw",
    user_agent="bot1")

#testing that it is the correct user
print(f"current user: {reddit.user.me()}")

#reddit url
#url = "https://www.reddit.com/r/UpliftingNews/comments/lemy1b/student_who_made_30k_from_gamestop_donates_games/"
#submission = reddit.submission(url=url)

'''
    table = []
    reply = []
    submission.comments.replace_more(limit=None) #replace all MoreComments objects with the actuall comments
    for sub in list(reddit.subreddit("wallstreetbets").top("all"))[:5]:
        posts = []
        #for top_level_comment in sub.comments.list(): #gets the subcomments of comments in a hierarchical order(First iterate subcomments then next comment)
        for top_level_comment in sub.comments[1:6]:
            if isinstance(top_level_comment, MoreComments) or top_level_comment.author == None:
                continue
            #posts.append(top_level_comment.body) #get comment's body
            for r in top_level_comment.replies:
                if isinstance(r, MoreComments):
                    continue
                reply.append(r.body)
            posts.append(top_level_comment.author.name) #get comment's redditor name 
        table.append(posts)
    posts = pd.DataFrame(table,columns=[str(i+1) for i in range(5)])
    print(posts)
    print(reply)
'''

#Make all posts*subreddits amount of nodes in the graph. The node labels are the post owners and the colors differ among subbredits  
def set_post_owners_nodes(Graph, subreddit_list, posts):
    for subreddit, color in subreddit_list:
        for post in list(reddit.subreddit(subreddit).top("month"))[:posts]:
            if post.author == None: #If post is deleted author = none
                continue
            Graph.add_node(post.author.name) #add the post's author name as node
            Graph.nodes[post.author.name]['created'] = datetime.fromtimestamp(post.created_utc) #set as attribute the post creation date
            Graph.nodes[post.author.name]['color'] = color #set as attribute the given color
    return Graph

def set_post_owners_edges(Graph, subreddit_list, posts = 20):
    Graph = set_post_owners_nodes(Graph, subreddit_list, posts)
    print(f"Post owners are {Graph.nodes}")
    for subreddit, color in subreddit_list:
        post_list = list(reddit.subreddit(subreddit).top("month"))[:posts] #A list of the first "posts" ammount of posts of the "subreddit" subreddit
        for post in post_list:
            post.comments.replace_more(limit=None) #replace all MoreComments objects with the actual comments
            for top_level_comment in post.comments:
                if top_level_comment.author == None: #If comment is deleted author = none
                    continue
                print(f"Post owner {post.author.name}. Comment owner {top_level_comment.author.name}")
                if top_level_comment.author.name in Graph.nodes:
                    #set directed edge that points from the user that has a post x and made a comment to post y, to the user of post y. Both x,y are in the same subreddit
                    Graph.add_edge(top_level_comment.author.name , post.author.name)
                    #set as attribute of this edge, the time of that comment
                    Graph[top_level_comment.author.name][post.author.name]['time'] = datetime.fromtimestamp(top_level_comment.created_utc)
    return Graph

#Top 5 Growing communities at 24/4/2022
#Color the nodes of each subreddit: red, blue, green, yellow, pink
Graph = nx.DiGraph()
subreddit_list = [("wallstreetbets","r"),("videos","b"),("tifu","g"), ("marvelstudios","y"),("Wellthatsucks","pink")] # 6-10 -> ["Weird","science","nottheonion","ChoosingBeggars","wow"]
Graph = set_post_owners_edges(Graph, subreddit_list) 

node_colors = [Graph.nodes[v]['color'] for v in Graph.nodes] #list of node colors
nx.write_gml(Graph, r'Graph.gml') #Save the graph in a file
#G = nx.read_gml(r'Graph.gml') To load the graph
nx.draw(Graph, with_labels=True, font_weight='bold', node_color = node_colors) #draw graph
plt.show()



#This script is for ploting data collected from "wallstreetbets".Top 20 posts collected of Month April day 24 
'''
User_Interaction_Graph = nx.DiGraph()
names = ['ThetaGang_wsb', 'ThePeppin', 'DipSnap', 'M0nk3y-K1ng', 'TomatilloAbject7419', '002timmy', 'DirtyDoeBoii', 'Zealousideal_Book151', 'swgaspar', 'justoneword_plastics', 'kdb2992', 'SupersonicMars', 'AbuelaOcasioCortez', 'thelongshortseller', 'Electrical-Message67', 'Unaheari', 'RawDick', 'ThanosTheBalanced', 'OreFortuner', 'keenfeed']
Interaction_Graph.add_nodes_from(names)
edges = [(4, 4), (4, 4), (8, 8), (11, 11), (12, 12), (5, 12), (13, 13), (13, 13), (13, 13), (13, 13), (16, 16), (13, 18)]
edge_list = [(names[i - 1], names[j - 1]) for i,j in edges]
Interaction_Graph.add_edges_from(edge_list)
nx.draw(Interaction_Graph, with_labels=True, font_weight='bold')
plt.show()
'''

