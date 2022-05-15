import praw

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
        self.node_list = []  # list contains STNode objects
        self.val = val

    def get_name(self):  # helper method to extract comments from tree in edgeList.py
        return self.val

    def get_replies(self):  # helper method to extract comments from tree in edgeList.py
        return self.node_list

    def insert(self, node):
        if self.val is not None:
            self.node_list.append(node)
            return self

        if self.val is None:
            self.val = val
            return self

    # prints the content of the STNode object and calls the method recursively for all the elements in STNode
    def preorder_output(self):
        # print(self.val)
        for subtree in self.node_list:
            subtree.preorder_output()
        return [self.val, self.node_list] #-> example [1 ,[[2,[5,6]],3,4]]


'''
sub.comments.list()
'''


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
    counter = 2
    post.comments.replace_more(limit=None)  # replace all MoreComments objects with the actual comments
    for comment in post.comments[:counter]:
        #if counter < 1:
            #break
        if comment.author is None:  # If comment is deleted author = none
            continue
        forest.append(make_tree(comment))
        #counter -= 1
    return forest


# returns a list of the top level authors as String and their repliers as STNode objects in a list
# return format of list: [ [author(String), [replies(STNode)] ]
def run():
    result = []
    for tree in make_forest(submission):
        result.append(tree.preorder_output())
    return result
