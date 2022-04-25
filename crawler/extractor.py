import pandas as pd
import praw
from praw.models import MoreComments

# use praw.ini file to initialize reddit object
reddit = praw.Reddit("bot1", user_agent="bot1 user agent")

# testing that it is the correct user
print(f"current user: {reddit.user.me()}")

# reddit url
# url = "https://www.reddit.com/r/UpliftingNews/comments/lemy1b/student_who_made_30k_from_gamestop_donates_games/"
#url = "https://www.reddit.com/r/wallstreetbets/comments/l6ea1b/what_are_your_moves_tomorrow_january_28_2021/"
url = "https://www.reddit.com/r/wallstreetbets/comments/u6khwq/so_i_just_quit_my_job_because_i_cant_take_the/"
submission = reddit.submission(url=url)

authors = []
# posts = []
authorsLevelOne = []
authorsLevelTwo = []

# extracting top level comments
#print(submission.authorsLevelOne.__len__())
# for top_level_comment in submission.comments[1:]:
#     if isinstance(top_level_comment, MoreComments):
#         continue
#     # authors.append(top_level_comment.author)
#     authorsLevelOne.append(top_level_comment.author)

# extracting first and second level comments
submission.comments.replace_more(limit=None)
for top_level_comment in submission.comments:
    # if isinstance(top_level_comment, MoreComments):
    #     continue
    for second_level_comment in top_level_comment.replies:
        # print(second_level_comment.body)
        # if isinstance(second_level_comment, MoreComments):
        #     continue
        authorsLevelTwo.append(second_level_comment.author)
        authorsLevelOne.append(top_level_comment.author)

# BFS over comment forest
# submission.comments.replace_more(limit=None)
# comment_queue = submission.comments[:]  # Seed with top-level
# while comment_queue:
#     comment = comment_queue.pop(0)
#     print(comment.author)
#     comment_queue.extend(comment.replies)

#easier version of BFS code from above
# submission.comments.replace_more(limit=None, threshold=0)
# for comment in submission.comments.list():
#     print(comment.author)

# putting lists in pandas df´s
commentsDF = pd.DataFrame(authorsLevelOne, columns=["property"])
comments2DF = pd.DataFrame(authorsLevelTwo, columns=["property"])
comments = pd.DataFrame(list(zip(authorsLevelOne, authorsLevelTwo)), columns=["comment author","reply author"])
# comments = pd.merge(commentsDF, comments2DF)

# output
# print(comments2DF)
print(comments)
# commentsDF.info()
# comments2DF.info()
