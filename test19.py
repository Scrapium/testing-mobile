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
from urllib.parse import urlparse, parse_qs, quote, urlencode
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

def get_guest_token():

    url = "https://api.twitter.com/1.1/guest/activate.json"
    headers = { 'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA' }

    response = requests.request("POST", url, headers=headers, data={})


def urlencode_noplus(query):

    return urlencode(query, safe='~')

def convert_dict(data):
    """Convert nested dictionaries into JSON strings."""
    new_dict = {}
    for key, value in data.items():
        if isinstance(value, dict):
            new_dict[key] = json.dumps(value).replace(' ', '%20')
        else:
            new_dict[key] = value
    return new_dict



class OAuth():
    """
    An OAuth authenticator.
    """
    def __init__(self, token, token_secret, consumer_key, consumer_secret):
        """
        Create the authenticator. If you are in the initial stages of
        the OAuth dance and don't yet have a token or token_secret,
        pass empty strings for these params.
        """
        self.token = token
        self.token_secret = token_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

        if token_secret is None or consumer_secret is None:
            raise MissingCredentialsError(
                'You must supply strings for token_secret and consumer_secret, not None.')

    def encode_params(self, base_url, method, params):
        params = params.copy()

        #if self.token:
        #    params['oauth_token'] = self.token

        #params['oauth_consumer_key'] = self.consumer_key
       # params['oauth_signature_method'] = 'HMAC-SHA1'
        #params['oauth_version'] = '1.0'
        ##params['oauth_timestamp'] = str(int(time.time()))
        #params['oauth_nonce'] = str(uuid.uuid4()).upper()

        #enc_params = urlencode_noplus(sorted(params.items()))
        #print(enc_params)

        #enc_params = urlencode(convert_dict(sorted(params.items())), safe='~', doseq=True)

        #converted_params = convert_dict(params)

        # URL encode the data
        #enc_params = urlencode(converted_params, safe='~', doseq=True)

        enc_params = urllib.parse.urlencode(params)
        #print(enc_params)


        # We use json.dumps() to convert the Python dicts to JSON format, 
        # making sure the booleans become `true`/`false` and strings are surrounded by `"`
        query_dict = {k: json.dumps(v) for k, v in params.items()}
        
        # Replace urllib.parse.urlencode with this
        query_string = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)


        print(enc_params)


        key = self.consumer_secret + "&" + urllib.parse.quote(self.token_secret, safe='~')

        message = '&'.join(
            urllib.parse.quote(i, safe='~') for i in [method.upper(), base_url, enc_params])
        


        signature = (base64.b64encode(hmac.new(
                    key.encode('ascii'), message.encode('ascii'), hashlib.sha1)
                                      .digest()))
        
        
    

        return signature

    def generate_headers(self):
        return {}

for oauth_consumer_key, oauth_consumer_secret, name in keys_and_secrets:

    oauth = OAuth1Session(oauth_consumer_key, client_secret=oauth_consumer_secret).fetch_request_token(request_token_url)

    oauth_token = oauth["oauth_token"]
    oauth_token_secret = oauth["oauth_token_secret"]


    https://api.twitter.com/oauth/authorize

