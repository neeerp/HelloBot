import praw
import pdb
import re
import os


if __name__ == "__main__":

    reddit = praw.Reddit("hello_bot")

    # Create/load a list of posts not to reply to in the future
    if not os.path.isfile("posts_replied_to.txt"):
        posts_replied_to = []
    else:
        with open("posts_replied_to.txt", "r") as f:
            posts_replied_to = f.read()
            posts_replied_to = posts_replied_to.split("\n")
            posts_replied_to = list(filter(None, posts_replied_to))

    # For the hottest 5 posts in r/neeerp
    subreddit = reddit.subreddit('neeerp')
    for submission in subreddit.hot(limit=5):

        # First, see if we should reply to the submission
        if submission.id not in posts_replied_to:
            if re.search("hello world", submission.selftext, re.IGNORECASE):
                submission.reply("Hello there!")
                posts_replied_to.append(submission.id)

        # Iterate through and reply to every comment that has "hello world"
        submission.comments.replace_more(limit=0)
        comment_queue = submission.comments[:]
        while comment_queue:
            comment = comment_queue.pop(0)
            comment_queue.extend(comment.replies)

            if comment.id not in posts_replied_to:
                if re.search("hello world", comment.body, re.IGNORECASE):
                    comment.reply("Hello there!")
                    posts_replied_to.append(comment.id)
    with open("posts_replied_to.txt", "w") as f:
        for post_id in posts_replied_to:
            f.write(post_id + "\n")
