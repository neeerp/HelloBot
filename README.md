# Hello Bot
A simple reddit bot written in python that scans the 5 hottest posts in a given subreddit and replies 'Hello there, /u/-user-' to every post/reply containing the string 'hello world'. Inspired by Shantnu Tiwari's guide at [Python for Engineers](pythonforengineers.com).

## Instructions

### Dependencies
This bot uses PRAW 5.2.1. Install it by typing
```
pip install praw
```
in your terminal

### Setting up a reddit account
In order to run Hello Bot, one must set up a reddit app. Create a new reddit account ( Or use an existing one if you please ), and browse to https://www.reddit.com/prefs/apps/. Scroll down and hit 'Create another app...'. Give it a name, select 'script', type in http://127.0.0.1 for the redirect uri, and hit create.

Now, you also need to set up a praw.ini file (either in the same directory as hello_bot.py, or in the config directory which is dependent on your operating system; see http://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html) to run Hello Bot. To the bottom of your config file, append the following:

```
[hello_bot]
client_id=<your app code>
client_secret=<your app secret>
password=<your reddit account's password>
username=<your reddit account's username>
user_agent=<user agent of your choice>
```
To elaborate, you can get your client id and secret from your app on reddit that you just set up. Your username and password is self explanatory, and your user agent can be something like 'Hello Bot'

### Running Hello Bot once
You can run Hello Bot from the command line by running
```
$ python hello_bot.py <subreddit>
```
Here, subreddit is whatever subreddit you'd like Hello Bot to look at. If you don't give a valid number of arguments, a message will be printed indicating this, and the subreddit will default to r/neeerp.

### Scheduling Hello Bot to run automatically
On a linux system, one may open crontab -e, and schedule the following:
```
* * * * * python path/from/home/to/hello_bot.py <subreddit>
```
If this fails to run, you may create a shell script that specifies the $PATH variable prior to running hello_bot and running that instead.

I personally haven't tested this on anything other than a server running ubuntu.


