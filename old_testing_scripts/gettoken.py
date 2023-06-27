from requests_oauthlib import OAuth1Session
import os
import webbrowser

# Set your consumer key and secret
consumer_key = "IQKbtAYlXLripLGPWd0HUA" # replace with your key as string if not setting environment variables
consumer_secret = "GgDYlkSvaPxGxC4X8liwpUoqKwwr3lCADbz8A7ADU" # replace with your secret as string if not setting environment variables

# Get a request token from Twitter
request_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError as e:
    print(e)
    print("There may have been an issue with the consumer_key or consumer_secret you entered.")
    
resource_owner_key = fetch_response.get('oauth_token')
resource_owner_secret = fetch_response.get('oauth_token_secret')
