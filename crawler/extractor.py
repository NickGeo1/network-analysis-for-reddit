import pandas as pd
import praw
from praw.models import MoreComments

# use praw.ini file to initialize reddit object
reddit = praw.Reddit("bot1", user_agent="bot1 user agent")

# testing that it is the correct user
print(f"current user: {reddit.user.me()}")

# reddit url
# url = "https://www.reddit.com/r/UpliftingNews/comments/lemy1b/student_who_made_30k_from_gamestop_donates_games/"
url = "https://www.reddit.com/r/wallstreetbets/comments/l6ea1b/what_are_your_moves_tomorrow_january_28_2021/"
submission = reddit.submission(url=url)

# extracting top level comments using "isinstance"-method
# for top_level_comment in submission.comments:
#     if isinstance(top_level_comment, MoreComments):
#         continue
#     print(top_level_comment.author.name)
#


authors = []
posts = []
comments = []
commentsLevelTwo = []

# extracting top level comments
print(submission.comments.__len__())
for top_level_comment in submission.comments[1:]:
    if isinstance(top_level_comment, MoreComments):
        continue
    authors.append(top_level_comment.author)
    comments.append(top_level_comment.body)

# extracting second level comments
submission.comments.replace_more(limit=0)
for top_level_comment in submission.comments:
    for second_level_comment in top_level_comment.replies:
        # print(second_level_comment.body)
        commentsLevelTwo.append(second_level_comment.body)

# putting lists in pandas df´s
commentsDF = pd.DataFrame(comments, columns=["body"])
comments2DF = pd.DataFrame(commentsLevelTwo, columns=["body"])

# output
# print(comments2DF)
# print(commentsDF)
commentsDF.info()
comments2DF.info()
