import time
import uuid
from requests_oauthlib import OAuth1Session

request_token_url = "https://api.twitter.com/oauth/request_token"

keys_and_secrets = [
    ("3rJOl1ODzm9yZy63FACdg", "5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8", "Mac")
]

for consumer_key, consumer_secret, name in keys_and_secrets:
    try:
        oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
        fetch_response = oauth.fetch_request_token(request_token_url)
        print(f"Fetch request token succeeded for {name}!")
        oauth_timestamp = int(time.time())
        oauth_nonce = uuid.uuid4()
        print("oauth_timestamp, " + str(oauth_timestamp))
        print("oauth_nonce, " + str(oauth_nonce))
        print(fetch_response)
    except Exception as e:
        print(f"Fetch request token failed for {name}. Error: {e}")
