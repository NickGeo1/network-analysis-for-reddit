# network-analysis-for-reddit


### Authentification
OAuth according to praw best practices using praw.ini file in local config directory
(https://praw.readthedocs.io/en/stable/getting_started/authentication.html#password-flow)

prawn.ini template:
https://praw.readthedocs.io/en/stable/getting_started/configuration/prawini.html#praw-ini

###Extraction
extraction of comments and sub-comments guide:
https://praw.readthedocs.io/en/stable/tutorials/comments.html

The submission object can return a CommentForest object which contains all top level comments and their corresponding sub-level comments as well
https://praw.readthedocs.io/en/stable/code_overview/other/commentforest.html#praw.models.comment_forest.CommentForest
