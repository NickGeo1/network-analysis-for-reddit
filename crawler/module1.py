import praw
import networkx as nx
import matplotlib.pyplot as plt

# use praw.ini file to initialize reddit object
reddit = praw.Reddit("bot1", user_agent="bot1 user agent")

# testing that it is the correct user
print(f"current user: {reddit.user.me()}")

# reddit url
url = "https://www.reddit.com/r/wallstreetbets/comments/u7wtfh/5k_to_100k_overnight_nflx_put/?utm_source=share" \
      "&utm_medium=web2x&context=3 "
submission = reddit.submission(url=url)

# Node of a tree with val as name of the comment author and list containing replies(children of the node)
class STNode:
    def __init__(self,  val=None):
        self.edge_list = []  # list contains directed edges from child to parent 
        self.node_list = []  # list contains STNode objects
        self.val = val

    def insert(self, node):
        if self.val is not None:
            self.node_list.append(node)
            return self

        if self.val is None:
            self.val = val
            return self

    # prints the content of the STNode object and calls the method recursively for all the elements in STNode
    def set_in_edges(self):
        for subtree in self.node_list:
            self.edge_list.append((subtree.val, self.val))
            subtree.set_in_edges()

# creates instance of STNode with comment author as root element and returns STNode instance
def make_tree(comment):
    root = STNode(comment.author.name)
    for reply in comment.replies:  # every 2nd level reply is child of comment
        if reply.author is None:  # If comment is deleted author = none
            continue
        root = root.insert(make_tree(reply))  # child element is again a STNode
    return root


# creates a tree for every top level comment and appends it to forest list and returns forest list
def make_forest(post):
    forest = []
    post.comments.replace_more(limit=None)  # replace all MoreComments objects with the actual comments
    for comment in post.comments:
        if comment.author is None:  # If comment is deleted author = none
            continue
        forest.append(make_tree(comment))
    return forest

graph = nx.DiGraph()
for tree in make_forest(submission):
    tree.set_in_edges()
    print(tree.edge_list)
    graph.add_edges_from(tree.edge_list)
    print()

nx.draw(graph, with_labels=True, font_weight='normal', node_size=100, font_size=8)  # TODO: node colors

# visualization
plt.show()  # TODO: styling of graph
# plt.savefig('first_three_comments.png', dpi=500)