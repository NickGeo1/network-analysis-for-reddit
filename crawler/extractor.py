import pandas as pd
import praw
from praw.models import MoreComments

#use praw.ini file to initialize reddit object
reddit = praw.Reddit("bot1", user_agent="bot1 user agent")

#testing that it is the correct user
print(f"current user: {reddit.user.me()}")

#reddit url
url = "https://www.reddit.com/r/UpliftingNews/comments/lemy1b/student_who_made_30k_from_gamestop_donates_games/"
submission = reddit.submission(url=url)

posts = []
for top_level_comment in submission.comments[1:]:
    if isinstance(top_level_comment, MoreComments):
        continue
    posts.append(top_level_comment.body)
posts = pd.DataFrame(posts,columns=["body"])
print(posts)

