import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import extractor2

authors = extractor2.run()  # get list of authors without structure

edgeList = []
#graph = nx.DiGraph()

def add_edges(authorlist):
    for lv0 in authorlist:  # for every comment author
        lv0Author = lv0[0]
        lv0Replies = lv0[1]
        # graph.add_node(lv0Author)
        for replyAuthor in lv0Replies:  # for every direct reply of the comment
            print(replyAuthor)
            print(lv0Author)
            print(lv0Replies)
            edgeList.append([lv0Author, replyAuthor.get_name()])
            add_edges([[replyAuthor.get_name(), replyAuthor.get_replies()]])  # TODO: brauch ich evtl nicht?


add_edges(authors)

df = pd.DataFrame(edgeList)
# print("----#-------------#----")
# print(df.head(50))

# for element in edgeList:
#     graph.add_edge(element[0],element[1])

#graph = nx.from_pandas_dataframe(df, 0, 1, True)
graph = nx.from_pandas_edgelist(df, 0, 1)

nx.write_gml(graph, r'Graph_new.gml')  # save graph to file
nx.draw(graph, with_labels=True, font_weight='bold')  # TODO: node colors
plt.show()

