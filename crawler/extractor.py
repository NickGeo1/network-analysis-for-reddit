import pandas as pd
import praw
from praw.models import MoreComments

#use praw.ini file to initialize reddit object
reddit = praw.Reddit("bot1", user_agent="bot1 user agent")

#testing that it is the correct user
print(f"current user: {reddit.user.me()}")

#reddit url
#url = "https://www.reddit.com/r/UpliftingNews/comments/lemy1b/student_who_made_30k_from_gamestop_donates_games/"
url = "https://www.reddit.com/r/wallstreetbets/comments/l6ea1b/what_are_your_moves_tomorrow_january_28_2021/"
submission = reddit.submission(url=url)

from praw.models import MoreComments

# for top_level_comment in submission.comments:
#     if isinstance(top_level_comment, MoreComments):
#         continue
#     print(top_level_comment.author.name)
#


authors = []
posts = []
comments = []

for top_level_comment in submission.comments[1:]:
    if isinstance(top_level_comment, MoreComments):
        continue
    authors.append(top_level_comment.author)
    comments.append(top_level_comment.body)
    

commentsDF = pd.DataFrame(comments, columns=["body"])
print(commentsDF)

