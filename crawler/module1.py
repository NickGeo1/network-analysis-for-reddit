import praw
import networkx as nx
import matplotlib.pyplot as plt
import time

# use praw.ini file to initialize reddit object
reddit = praw.Reddit("bot1", user_agent="bot1 user agent")

# testing that it is the correct user
print(f"current user: {reddit.user.me()}")

# reddit url
url = "https://www.reddit.com/r/wallstreetbets/comments/u7wtfh/5k_to_100k_overnight_nflx_put/?utm_source=share" \
      "&utm_medium=web2x&context=3 "
submission = reddit.submission(url=url)

def make_tree(comment):
    single_comment_edges = []
    for reply in comment.replies:  # every 2nd level reply is child of comment
        if reply.author is None:  # If comment is deleted author = none
            continue
        single_comment_edges += [(reply.author.name, comment.author.name)]
        single_comment_edges += make_tree(reply)
    return single_comment_edges


# creates a tree for every top level comment and appends it to forest list and returns forest list
def make_forest(post):
    forest = []
    post.comments.replace_more(limit=None)  # replace all MoreComments objects with the actual comments
    for comment in post.comments[:2]:
        if comment.author is None:  # If comment is deleted author = none
            continue
        forest += make_tree(comment)
    return forest

before = time.time()
graph = nx.DiGraph()
graph.add_edges_from(make_forest(submission))
nx.draw(graph, with_labels=True, font_weight='normal', node_size=100, font_size=8)  # TODO: node colors
print(f"time: {time.time() - before}")
# visualization
plt.show()  # TODO: styling of graph
# plt.savefig('first_three_comments.png', dpi=500)