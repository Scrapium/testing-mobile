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

from urllib.parse import urlparse, parse_qs, quote

CONSUMER_SECRET = "5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8"
CONSUMER_KEY = "3rJOl1ODzm9yZy63FACdg"
oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET).fetch_request_token("https://api.twitter.com/oauth/request_token")
oauth_token = oauth["oauth_token"]
oauth_token_secret = oauth["oauth_token_secret"]


def sign_request(consumer_secret, token_secret, base_string):
    from hashlib import sha1
    import hmac

    # key = b"CONSUMER_SECRET&" #If you dont have a token yet
    # "CONSUMER_SECRET&TOKEN_SECRET" 
    key = bytes("{}&{}".format(consumer_secret, token_secret), encoding='utf8' )


    # The Base String as specified here: 
    raw = bytes("{}".format(base_string), encoding='utf8' ) # as specified by OAuth
       
    hashed = hmac.new(key, raw, sha1)
    
    # The signature
    b64hash = b64encode(hashed.digest()).decode('utf-8') #hashed.digest().encode("base64").rstrip('\n')


    return urllib.parse.quote_plus(b64hash)

def do_req():

    oauth_timestamp = str(int(time.time()))


    method = "GET"
    path = "https://api.twitter.com/graphql/pAyVFRiMFMp9KCfffF7LHg/HomeLatestTimeline"
    params = {
         'oauth_consumer_key': CONSUMER_KEY,
         'oauth_nonce': '	yzZhVMzDDR1',
         'oauth_signature_method': 'HMAC-SHA1',
         'oauth_timestamp': oauth_timestamp,
         'oauth_token': oauth_token,
         'oauth_version': '1.0'
    }

    # important

    request_params_web = urllib.parse.urlencode(params)
    message = "GET&" + urllib.parse.quote_plus(path) + urllib.parse.quote_plus(request_params_web)
    signature = sign_request(CONSUMER_SECRET, oauth_token_secret, message)

    print(signature)

    import requests

    url = "https://api.twitter.com/graphql/pAyVFRiMFMp9KCfffF7LHg/HomeLatestTimeline"


    # debugging with magic variables

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'OAuth oauth_consumer_key="3rJOl1ODzm9yZy63FACdg",oauth_signature_method="HMAC-SHA1",oauth_timestamp="' + str(oauth_timestamp) + '",oauth_nonce="yzZhVMzDDR1",oauth_version="1.0",oauth_signature="' + signature + '"',
    }


    
    print(headers["Authorization"])
    #OAuth oauth_consumer_key="3rJOl1ODzm9yZy63FACdg",oauth_signature_method="HMAC-SHA1",oauth_timestamp="1687706987",oauth_nonce="yzZhVMzDDR1",oauth_version="1.0",oauth_signature="y4cZSyg9mMQ3fS%2Fe2tvLqQySMYk%3D"

    #OAuth oauth_consumer_key="3rJOl1ODzm9yZy63FACdg",oauth_signature_method="HMAC-SHA1",oauth_timestamp="1687705030",oauth_nonce="yzZhVMzDDR1",oauth_version="1.0",oauth_signature="RBxrZUsiTOiI9NC87%2F0%2FLjGWxSI%3D"


    response = requests.request("GET", url, headers=headers, data={})

    print(response.text)


#%2Fo8fiK5saCKw%2FCh260%2FS%2FwSH5X8%3D
#mY4%2BH6muSZXurIcCvG1LiU750bA%3D
do_req()

