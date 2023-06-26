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
from twitter import *

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

    oauth_send_token = get_guest_token() + "-" + oauth_token
   
    t = Twitter(auth=OAuth(oauth_send_token, oauth_token_secret, oauth_consumer_key, oauth_consumer_secret))

    object_methods = [method_name for method_name in dir(t)
                  if callable(getattr(t, method_name))]

    print(object_methods)

    #t.search.tweets(q="#pycon")