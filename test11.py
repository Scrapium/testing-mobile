import time
import uuid
from requests_oauthlib import OAuth1Session
import urllib
import hmac
import hashlib
import base64
import urllib
import requests
import json
from collections import OrderedDict

import http.client
import secrets
import hashlib
import hmac
import re
import urllib
from random import getrandbits
from urllib.parse import urlparse, parse_qs, quote


def enc(text):
    return urllib.parse.quote(text, safe='')
    
request_token_url = "https://api.twitter.com/oauth/request_token"

keys_and_secrets = [
    #("3nVuSoBZnx6U4vzUxf5w", "Bcs59EFbbsdF6Sl9Ng71smgStWEGwXXKSjYvPVt7qys", "Android"),
    #("IQKbtAYlXLripLGPWd0HUA", "GgDYlkSvaPxGxC4X8liwpUoqKwwr3lCADbz8A7ADU", "iPhone"),
    #("CjulERsDeqhhjSme66ECg", "IQWdVyqFxghAtURHGeGiWAsmCAGmdW3WmbEx6Hck", "iPad"),
    ("3rJOl1ODzm9yZy63FACdg", "5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8", "Mac"),
    #("yN3DUNVO0Me63IAQdhTfCA", "c768oTKdzAjIYCmpSNIdZbGaG0t6rOhSFQP0S5uC79g", "Windows Phone"),
    #("iAtYJ4HpUVfIUoNnif1DA", "172fOpzuZoYzNYaU3mMYvE8m8MEyLbztOdbrUolU", "Google TV"),
    #("yT577ApRtZw51q4NPMPPOQ", "3neq3XqN5fO3obqwZoajavGFCUrC42ZfbrLXy5sCv8", "TweetDeck"),
    #("TgHNMa7WZE7Cxi1JbkAMQ", "SHy9mBMBPNj3Y17et9BF4g5XeqS4y3vkeW24PttDcY", "Windows"),
    #("RwYLhxGZpMqsWZENFVw", "Jk80YVGqc7Iz1IDEjCI6x3ExMSBnGjzBAH6qHcWJlo", "Android Sign-Up"),
    #("8AeR93em84Pyum5i1QGA", "ugCImRuw376Y9t9apIq6bgWGNbb1ymBrx2K5NK0ZI", "Tweetbot for iOS"),
    #("WfEZ02WzcqZMvs4HJMZLA", "69zIxwA9KSuY4IDYRT2Bfk1rq62Nq1csspXOfSRKhg", "YoruFukurou"),
    #("w1Gybt9LP9zG46mS1X3UAw", "hRIK4RWjAO4pokQCvmNCynRAY8Jc8edV1kcV2go6g", "HootSuite"),
    #("Eb8hyAEUju1f2g0i2iSwTQ", "lOBgiyGJcYK4jsUc2It38ORlsJC0a60USShZrosMTlw", "ShootingStar"),
    #("I8ye5YHbnFUVzrWdyEkXw", "UTXlrSs9IuZuhfxfwBDckzMDHCI8HRlTNtitiV2OL4", "ShootingStarPro"),
    #("7S2l5rQTuFCj4YJpF7xuTQ", "L9VHCXMKBPb2eWjvRvQTOEmOyGlH4W50getaQJPya4", "twicca"),
    #("lYa4VucwdoUUTQLC2utgtg", "NfnIALNRMcrvC844yypUubWp2xmuiL3zbLN8osjWntM", "Twitcle"),
    #("yqoymTNrS9ZDGsBnlFhIuw", "OMai1whT3sT3XMskI7DZ7xiju5i5rAYJnxSEHaKYvEs", "Echofon"),
    #("7YBPrscvh0RIThrWYVeGg", "sMO1vDyJ9A0xfOE6RyWNjhTUS1sNqsa7Ae14gOZnw", "Instagram")
]

def generate_random_nonce():
    return str(uuid.uuid4()).upper()

def get_guest_token():

    url = "https://api.twitter.com/1.1/guest/activate.json"
    headers = { 'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA' }

    response = requests.request("POST", url, headers=headers, data={})

    return json.loads(response.text)["guest_token"]

"""
    def sign_request():
        from hashlib import sha1
        import hmac

        # key = b"CONSUMER_SECRET&" #If you dont have a token yet
        key = b"CONSUMER_SECRET&TOKEN_SECRET" 


        # The Base String as specified here: 
        raw = b"BASE_STRING" # as specified by OAuth
           
        hashed = hmac.new(key, raw, sha1)
        
        # The signature
        return hashed.digest().encode("base64").rstrip('\n')
"""

def enc2(value):
    if isinstance(value, dict):
        value = json.dumps(value)
    return urllib.parse.quote(value, safe='')

def sign_request(consumer_secret, oauth_token_secret, raw):
    # key = b"CONSUMER_SECRET&oauth_token_secret" #
    key = consumer_secret.encode() + b"&" + oauth_token_secret.encode()

    hashed = hmac.new(key, raw, hashlib.sha1)

    # The signature
    return base64.b64encode(hashed.digest())


def dict_to_string(oauth_dict):
    pairs = []
    for key, value in oauth_dict.items():
        pair = f'{key}="{value}"'
        pairs.append(pair)
    oauth_string = "OAuth " + ", ".join(pairs)
    return oauth_string


def dict_to_string2(oauth_dict):
    pairs = []
    for key, value in oauth_dict.items():
        pair = f'{key}="{value}"'
        pairs.append(pair)
    oauth_string = ", ".join(pairs)
    return oauth_string

for oauth_consumer_key, oauth_consumer_secret, name in keys_and_secrets:

    oauth = OAuth1Session(oauth_consumer_key, client_secret=oauth_consumer_secret).fetch_request_token(request_token_url)

    oauth_token = oauth["oauth_token"]
    oauth_token_secret = oauth["oauth_token_secret"]

    print(oauth_consumer_key)
    print(oauth_consumer_secret)
    print(oauth_token)
    print(oauth_token_secret)
   

    guest_token = get_guest_token()
    
    oauth_nonce = generate_random_nonce()
    oauth_timestamp = str(int(time.time()))

    print("oauth_consumer_key: " + str(oauth_consumer_key))
    print("oauth_consumer_secret: " + str(oauth_consumer_secret))
    print("oauth_token: " + str(oauth_token))
    print("oauth_token_secret: " + str(oauth_token_secret))

    oauth_send_token = get_guest_token() + "-" + "iOiY4xgK8K3oG2rl4QevBOWktkCXPI"
    #oauth_send_token = get_guest_token() + "-" + oauth_token

    #print("oauth_send_token: " + str(oauth_send_token))
    #print("oauth_send_token2: " + str(oauth_send_token2))


    """
        sig_headers = {
                'oauth_signature': 'OSpMkX7U2JgVtNeKIve4lXhb1T4%3D', 
                'oauth_nonce': '44189BB8-FA49-41B6-B9AB-2EC7D46416C8', 
                'oauth_timestamp': '1687621205', 
                'oauth_consumer_key': 'IQKbtAYlXLripLGPWd0HUA', 
                'oauth_token': '1672630233671823361-iOiY4xgK8K3oG2rl4QevBOWktkCXPI', 
                'oauth_version': '1.0', 
                'oauth_signature_method': 'HMAC-SHA1'
        }
    """


    # OAuth oauth_signature="OSpMkX7U2JgVtNeKIve4lXhb1T4%3D", oauth_nonce="44189BB8-FA49-41B6-B9AB-2EC7D46416C8", oauth_timestamp="1687621205", oauth_consumer_key="IQKbtAYlXLripLGPWd0HUA", oauth_token="1672630233671823361-iOiY4xgK8K3oG2rl4QevBOWktkCXPI", oauth_version="1.0", oauth_signature_method="HMAC-SHA1"
    # OAuth oauth_signature="fQF1HBa0QGer0WnVjW39UY3OayI%3D", oauth_nonce="44189BB8-FA49-41B6-B9AB-2EC7D46416C8", oauth_timestamp="1687621205", oauth_consumer_key="IQKbtAYlXLripLGPWd0HUA", oauth_token="1672630233671823361-iOiY4xgK8K3oG2rl4QevBOWktkCXPI", oauth_version="1.0", oauth_signature_method="HMAC-SHA1"'
    sig_headers = dict(sorted({
            'oauth_nonce': str(oauth_nonce), 
            'oauth_timestamp': str(oauth_timestamp),
            'oauth_consumer_key': str(oauth_consumer_key), 
            'oauth_token': str(oauth_send_token), 
            'oauth_version': '1.0', 
            'oauth_signature_method': 'HMAC-SHA1'
    }.items(), key=lambda x: x[0]))

    ####


    url = "https://api.twitter.com/graphql/pAyVFRiMFMp9KCfffF7LHg/HomeLatestTimeline"


    databeforeEnc = "GET&" + enc("https://api.twitter.com/graphql/pAyVFRiMFMp9KCfffF7LHg/HomeLatestTimeline") + "&" + enc2(urllib.parse.urlencode(sig_headers))



    #GET&https%3A%2F%2Fapi.twitter.com%2Fgraphql%2FpAyVFRiMFMp9KCfffF7LHg%2FHomeLatestTimeline&oauth_consumer_key%3D3rJOl1ODzm9yZy63FACdg%26oauth_nonce%3D5DD22912-58EF-4FCD-87CC-135BB55B2C4D%26oauth_signature_method%3DHMAC-SHA1%26oauth_timestamp%3D1687661819%26oauth_token%3D1672801061097144322-stqEwAAAAAAACIKFAAABiPB70Tg%26oauth_version%3D1.0
    #POST&https%3A%2F%2Fapi.twitter.com%2F1.1%2Fstatuses%2Fdestroy%2F{}.json&oauth_consumer_key%3DIQKbtAYlXLripLGPWd0HUA%26oauth_nonce%3D133333333337%26oauth_signature_method%3DHMAC-SHA1%26oauth_timestamp%3D1631907844%26oauth_token%3D{}%26oauth_version%3D1.0

    print(databeforeEnc)

    oauth_consumer_secret = sig_headers['oauth_consumer_key'] # replace with your actual secret
    oauth_token_secret = sig_headers['oauth_token'] # replace with your actual token secret

    key = oauth_consumer_secret + "&{}".format(oauth_token_secret)
    key = key.encode('utf-8') # convert key to bytes

    # Ensure that your databeforeEnc variable is in bytes
    databeforeEnc = databeforeEnc.encode('utf-8')

    # Compute the signature
    signature = hmac.new(key, msg=databeforeEnc, digestmod=hashlib.sha1).digest()
    signature = base64.b64encode(signature).decode('utf-8') # base64 encode and convert to string

    # URL encode the signature
    signature = urllib.request.pathname2url(signature)

    sig_headers["oauth_signature"] = signature

    ####

    req_headers = { 
            'Connection': 'close', 'X-Twitter-Client-Language': 'en',
            'Content-Type': 'application/x-www-form-urlencoded', 
            'Host': 'api.twitter.com',
            'User-Agent': 'Chromium/1.0',
            "Authorization": dict_to_string( sig_headers)
    }

    print(req_headers)

    

    

    print(req_headers)

    
    payload = {'grant_type': 'client_credentials'}
    response = requests.request("GET", url, headers=req_headers, data=payload)

    print(response.text)


