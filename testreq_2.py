import tweepy

oauth = OAuth1UserHandler(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    callback="oob"
)

twitter_url = oauth.get_authorization_url(signin_with_twitter=True)