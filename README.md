# network-analysis-for-reddit


### Authentification
OAuth according to praw best practices using praw.ini file in local config directory
(https://praw.readthedocs.io/en/stable/getting_started/authentication.html#password-flow)

prawn.ini template:
https://praw.readthedocs.io/en/stable/getting_started/configuration/prawini.html#praw-ini

### Content
- Code implemented to call reddit api and extract comments from various posts of WallStreetBets subreddit
- Code implemented to make the comments graph with NetworkX library and extract the data in a txt file
- Gephi Software files representing versions of graphs
- Final report of the assignment(read this for project details)

### Task

Please note that we approached the problem in a different way: 

- We considered posts(instead of blogs) as clusters and user comments(instead of posts) as nodes. 
- Two user-nodes are connected with an edge if one user replies to another.

Choose an active blog community of your choice with an available API to ease data collection.
Proceed in the following way to construct the social network graph.

-Start with a list of most cited blogs at a specific time of your choice and select a time window (it
should include the time of most cited blog) that you can use to collect posts and blogs occurring
within that time interval.

-Make some reasonable assumptions in terms of the maximum number of posts that will be
retrieved.

-Typically, each post contains a link of the parent blog, date of the post, post content and a list of
all links that occur in the post’s content.

1. Elaborate on the choice of blogs and size of data collection.
2. Plot the number of posts per day over the span of the collected dataset
3. We would like to represent the collected data as a cluster graph where clusters correspond to
blogs, nodes in the cluster are posts from the blog, and hyper-links between posts in the dataset
are represented as directed edges. Only consider out-links to posts in the dataset. Therefore,
remove links that point to posts outside the collected dataset or other resources on the web
(images, movies, other web-pages), and also those edges that point to themselves if any. This is
to keep track of timestamp for temporal analysis.
4. Study the global properties of the established network: number of noes, number of edges,
clustering coefficient, diameter, size of giant component, average in-degree centrality and out-
degree centrality and their associated variance, average path length and its variance, average
closeness centrality and its variance, average in-betweeness centrality and its variance.
5. Trace the in-degree centrality distribution and check whether a power-law distribution can be fit
using appropriate statistical testing
6. Trace the out-degree centrality distribution and check whether a power-law distribution can be
fit using appropriate statistical testing
7. Now investigate the temporal variation of popularity. For this purpose, collect all in-links to a post
and plot the number of links occurring after each day following the post. This creates a curve that
indicates the rise and fall of popularity. By aggregating over a large set of posts, you should a
obtain a more general pattern.
8. Check whether a power-law distribution can be fit
9. identify appropriate literature to comment on the obtained results and the limitations
