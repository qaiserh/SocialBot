SocialBot
SocialBot - Documentation

SocialBot is a webapp that lets you schedule tweets and facebook posts to be posted
at a later date. Use it to stagger your posts so that your friends don't get
sick of you! Or, alternatively, use it to advertise in an unobnoxious way, by
staggering sponsored posts. 

1) Running
2) Features
3) Code

*-*
Since the app depends on callbacks from Facebook and twitter you can't really run it locally because the callback urls point to socialbot.herokuapp.com
*-*

1) Running the app is simple. Go to socialbot.herokuapp.com to access it. Click on
one of the big buttons to authenticate with either Facebook or Twitter. Then post away.

2) The app allows you to schedule posts for both Twitter and Facebook. A validation
check makes sure all tweets are under 140 characters.  We also make a validation for the 
presence of a scheduled time. The app can post at any time in
the future, and can queue multiple posts for Twitter and Facebook.

All scheduled tweets are visible on the tweets page, just as all scheduled statuses
are visible on the Facebook page. These statuses and tweets can be edited or deleted
before they are published, in case the user changes his/her mind.

Once you have authorized the app with Facebook and Twitter, the app also automatically
signs you in if you are signed into both services on that computer.

3) The code is divided into app.py, scheduler.py and a series of templates for the
various webpages. app.py contains the methods that handle initial login and user
authentication, as well as the methods that add tweets and statuses to the SimpleDB
database we have set up. It also contains the edit/delete method. We maintain local dictionaries
corresponding to the data in the database to minimize queries to the database and to
make sure scheduled tweets, statuses display quickly.

scheduler.py contains the code responsible for posting at the scheduled times. Posting
at the exact times would be incredibly taxing, so instead scheduler.py queries the
database every 10 minutes, and checks if any posts were timed before the current time.
So it posts in waves separated by 10 minutes using Heroku's Scheduler.

We use Twitter Bootstrap for design and Jinja2 to populate the templates with data
and interact with our python code.

TODO:
- Add support for different timezones
