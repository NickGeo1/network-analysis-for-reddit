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

class STNode:
    def __init__(self,  val=None):
        self.node_list = [] #list contains STNode objects
        self.val = val

    def insert(self, node):
        if self.val is not None:
            self.node_list.append(node)
            return self

        if self.val is None:
            self.val = val
            return self

    def PreorderOutput(self):
        print(self.val)
        for subtree in self.node_list:
            subtree.PreorderOutput()


#testing that it is the correct user
print(f"current user: {reddit.user.me()}")

#reddit url
url = "https://www.reddit.com/r/wallstreetbets/comments/u7wtfh/5k_to_100k_overnight_nflx_put/?utm_source=share&utm_medium=web2x&context=3"
submission = reddit.submission(url=url)

'''
sub.comments.list()
'''

def Make_tree(comment):
    root = STNode(comment.author.name)
    for reply in comment.replies:
        if reply.author == None: #If comment is deleted author = none
            continue
        root = root.insert(Make_tree(reply))
    return root

def Make_forest(post):
    Forest = []
    post.comments.replace_more(limit=None) #replace all MoreComments objects with the actual comments
    for comment in post.comments:
        if comment.author == None: #If comment is deleted author = none
            continue
        Forest.append(Make_tree(comment))
    return Forest
#Make_forest(submission)

for tree in Make_forest(submission):
    tree.PreorderOutput()
    print()


