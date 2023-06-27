from random import getrandbits
from base64 import b64encode
from time import time
import urllib
import hmac
from hashlib import sha1
import urllib
from requests_oauthlib import OAuth1Session
import time
import oauth2 as oauth
import json
import requests
import uuid
import datetime

from urllib.parse import urlparse, parse_qs, quote

CONSUMER_SECRET = "5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8"
CONSUMER_KEY = "3rJOl1ODzm9yZy63FACdg"
oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET).fetch_request_token("https://api.twitter.com/oauth/request_token")
oauth_token = oauth["oauth_token"]
oauth_token_secret = oauth["oauth_token_secret"]


def sign_request(oauth_token_secret,raw):
    # key = b"CONSUMER_SECRET&oauth_token_secret" #
    key = b"GgDYlkSvaPxGxC4X8liwpUoqKwwr3lCADbz8A7ADU&"+oauth_token_secret.encode()

    hashed = hmac.new(key, raw, sha1)

    # The signature
    return b64encode(hashed.digest())



def takefirti(oauth_token_secret,oauth_token):
    nonce = str(uuid.uuid4())
    time1 = str(int(time.time()))
    databeforeEnc = "GET&https%3A%2F%2Fapi.twitter.com%2Fgraphql%2FpAyVFRiMFMp9KCfffF7LHg%2FHomeLatestTimeline%3Foauth_consumer_key%3D3rJOl1ODzm9yZy63FACdg%26oauth_nonce%3D133333333337%26oauth_signature_method%3DHMAC-SHA1%26oauth_timestamp%3D%7B%7D%26oauth_token%3D%7B%7D%26oauth_version%3D1.0".format(
        time1,oauth_token)

    sig = sign_request(oauth_token_secret,databeforeEnc.encode()).decode().replace("=", "%3D")

    print(sig)

    headers = {'Connection': 'close', 'X-Twitter-Client-Language': 'en',
                   'Content-Type': 'application/x-www-form-urlencoded', 'Host': 'api.twitter.com',
                   'Authorization': 'OAuth oauth_signature="{}", oauth_nonce="{}", oauth_timestamp="{}", oauth_consumer_key="3rJOl1ODzm9yZy63FACdg", oauth_token="{}", oauth_version="1.0", oauth_signature_method="HMAC-SHA1"'.format(
                       nonce, sig,time1, oauth_token)}
    _sig = urllib.parse.quote(sig)

    print(_sig)

    test = "https://api.twitter.com/graphql/pAyVFRiMFMp9KCfffF7LHg/HomeLatestTimeline?oauth_consumer_key=3rJOl1ODzm9yZy63FACdg&oauth_nonce={}&oauth_signature_method=HMAC-SHA1&oauth_timestamp={}&oauth_token={}&oauth_version=1.0&oauth_signature={}".format(nonce, time1,oauth_token, _sig)

    print(test)

    req1 = requests.get(test, headers=headers)
    print(req1.text)


takefirti(oauth_token_secret, oauth_token)
#RBxrZUsiTOiI9NC87%2F0%2FLjGWxSI%3D
#KXbNlz8Z5nSDmIuFpqTUGaf%2Fyik%253D