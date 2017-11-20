import praw
import re
import os
import sys


class HelloBot:
    """
        A reddit bot that scans the 5 hottest submissions in a subreddit and
        replies to all posts containing the string 'hello world' with
        'Hello there!'.
    """
    def __init__(self):
        """
            Initialize Hello bot, loading in its list of posts to ignore and
            preparing an instance of praw.Reddit
        """
        self._reddit = praw.Reddit('hello_bot')

        # Initialize or load a list containing the posts Hellobot should ignore
        if not os.path.isfile('posts_replied_to.txt'):
            self._posts_replied_to = []
        else:
            with open('posts_replied_to.txt', 'r') as f:
                post_string = f.read()
                self._posts_replied_to = post_string.split("\n")
                self._posts_replied_to = \
                    list(filter(None, self._posts_replied_to))

    def _update_replied_to(self):
        """ Update the file list of posts hellobot has replied to """
        with open('posts_replied_to.txt', 'w') as f:
            for post_id in self._posts_replied_to:
                f.write(post_id + '\n')

    def _reply_to_post(self, post):
        """
            First, check to see if the post is a comment or submission, then
            reply if its text contains 'hello world' and hellobot hasn't
            already replied!

            :param post: The post that hellobot will parse and maybe reply to
            :type post: praw.Submission || praw.Comment
        """

        if isinstance(post, praw.models.Submission):
            post_text = post.selftext
        else:
            post_text = post.body

        if post.id not in self._posts_replied_to and \
                re.search('hello world', post_text, re.IGNORECASE):

            post.reply('Hello there, /u/%s!' % post.author.name)
            self._posts_replied_to.append(post.id)

    def _check_comment_tree(self, submission):
        """
            Iterate over a submission's comment tree, replying to each
            applicable comment.

            :param submission: The comment tree to iterate over
            :type submission: praw.Submission
        """
        # Get rid of 'uncollapsed' comments
        submission.comments.replace_more(limit=0)

        comment_queue = submission.comments[:]
        while comment_queue:
            comment = comment_queue.pop(0)
            comment_queue.extend(comment.replies)

            self._reply_to_post(comment)

    def say_hello(self, subreddit):
        """
            Iterate through the 5 hottest submissions in a given subreddit
            and have hellobot say hello to any posts (comments OR submissions)
            containing the string 'hello world'.

            :param subreddit: The subreddit to check
            :type subreddit: str
        """
        for submission in self._reddit.subreddit(subreddit).hot(limit=5):
            self._reply_to_post(submission)
            self._check_comment_tree(submission)
        self._update_replied_to()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        subreddit = sys.argv[1]
    else:
        print("Invalid arguments given; defaulting to subreddit r/neeerp")
        subreddit = 'neeerp'

    hello_bot = HelloBot()
    hello_bot.say_hello(subreddit)
