import commentExtractor

edgeList = []  #


# method that extracts comment and replier names from the authors list and appends edges to edgeList
def add_edges(authorlist):
    for lv0 in authorlist:  # for every comment author
        lv0Author = lv0[0]
        lv0Replies = lv0[1]
        # graph.add_node(lv0Author)
        for replyAuthor in lv0Replies:  # for every direct reply of the comment
            edgeList.append([lv0Author, replyAuthor.get_name()])
            add_edges([[replyAuthor.get_name(), replyAuthor.get_replies()]])  # recursive call of method to get replies


def run():
    authors = commentExtractor.run()  # get list of authors without structure
    add_edges(authors)  # create list of edges in format [ [origin_node, target_node] ]
    return edgeList
