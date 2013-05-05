import boto
import datetime
from flask import Flask
from flask_oauth import OAuth


FACEBOOK_APP_ID = '163882543775188'
FACEBOOK_APP_SECRET = 'ENTER FACEBOOK APP_SECRET'

TWITTER_APP_ID = 'jZlGiwREwsKBHcliO0ZKGg'
TWITTER_APP_SECRET = 'ENTER TWITTER APP_SECRET'

oauth = OAuth()

app = Flask(__name__)

app.config.update(
    DEBUG = True,
)
app.secret_key = '\xc7\xc0tj\xee\x0e-\x98n\x0bh\x00nZ\x81\x01\x83\xbe\xcdzX\xd8\x1ei'

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key= FACEBOOK_APP_ID,
    consumer_secret= FACEBOOK_APP_SECRET,
    request_token_params={'scope': ('email, publish_actions')}
)

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key= TWITTER_APP_ID,
    consumer_secret= TWITTER_APP_SECRET
)

sdb = boto.connect_sdb('ENTER AWS KEY', 'ENTER AWS SECRET KEY')

domain = sdb.get_domain('socialbot')

@facebook.tokengetter
def get_facebook_token(token=None):
	user = domain.get_item(token)
	if user is None:
		raise Exception
	return (user['facebook_token'], '')
    
@twitter.tokengetter
def get_twitter_token(token=None):
	user = domain.get_item(token)
	if user is None:
		raise Exception
	print user.name
	return (user['oauth_token'], user['oauth_token_secret'])

def main():
	"""
		This method checks in the database if there are any tweets
		or statuses scheduled for the next 10 minutes. If there are,
		it posts those one by one.

	"""
	now = datetime.datetime.now()
	future = (now + datetime.timedelta(minutes = 10)).strftime("%Y%m%d%H%M%S")
	item_iterator = domain.select("select * from socialbot where time < '" + str(future) + "'")
	
	for item in item_iterator:
		print str(item)
		user = item['user_id']
		if item['type'] == 'facebook':
			resp = facebook.post('/me/feed', data = {'message': item['message']}, token = user)
			if resp.status != 200:
				print "Woops, something went wrong when trying to post this status #{item['message']}"
		else:
			resp = twitter.post('statuses/update.json', data={'status': item['message']}, token = user)
			if resp.status != 200:
				print "Woops, something went wrong when trying to post this tweet #{item['message']}"

		domain.delete_item(item)

if __name__ == "__main__":
	main()





