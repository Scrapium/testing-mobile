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


for oauth_consumer_key, oauth_consumer_secret, name in keys_and_secrets:

    oauth = OAuth1Session(oauth_consumer_key, client_secret=oauth_consumer_secret).fetch_request_token(request_token_url)

    oauth_token = oauth["oauth_token"]
    oauth_token_secret = oauth["oauth_token_secret"]
    guest_token = get_guest_token()
    
    oauth_nonce = generate_random_nonce()
    oauth_timestamp = str(int(time.time()))

    print("oauth_consumer_key: " + str(oauth_consumer_key))
    print("oauth_consumer_secret: " + str(oauth_consumer_secret))
    print("oauth_token: " + str(oauth_token))
    print("oauth_token_secret: " + str(oauth_token_secret))

    #oauth_send_token2 = get_guest_token() + "-" + "iOiY4xgK8K3oG2rl4QevBOWktkCXPI"
    oauth_send_token = get_guest_token() + "-" + oauth_token

    #print("oauth_send_token: " + str(oauth_send_token))
    #print("oauth_send_token2: " + str(oauth_send_token2))



    headers = {
            'oauth_signature': 'OSpMkX7U2JgVtNeKIve4lXhb1T4%3D', 
            'oauth_nonce': '44189BB8-FA49-41B6-B9AB-2EC7D46416C8', 
            'oauth_timestamp': '1687621205', 
            'oauth_consumer_key': 'IQKbtAYlXLripLGPWd0HUA', 
            'oauth_token': '1672630233671823361-iOiY4xgK8K3oG2rl4QevBOWktkCXPI', 
            'oauth_version': '1.0', 
            'oauth_signature_method': 'HMAC-SHA1'
    }

    req_headers = { "Authorization": dict_to_string(headers) }

    url = "https://api.twitter.com/graphql/pAyVFRiMFMp9KCfffF7LHg/HomeLatestTimeline?features=%7B%22graphql_unified_card_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22unified_cards_ad_metadata_container_dynamic_card_content_query_enabled%22%3Atrue%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22trusted_friends_api_enabled%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Afalse%2C%22birdwatch_consumption_enabled%22%3Afalse%2C%22tweet_with_visibility_results_prefer_gql_tweet_interstitials_enabled%22%3Atrue%2C%22profile_foundations_has_spaces_graphql_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Afalse%2C%22rito_safety_mode_features_enabled%22%3Afalse%2C%22tweet_awards_tweet_api_enabled%22%3Afalse%2C%22ios_notifications_replies_mentions_device_follow_enabled%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_soft_interventions_enabled%22%3Atrue%7D&variables=%7B%22latest_control_available%22%3Atrue%2C%22include_community_tweet_relationship%22%3Afalse%2C%22request_context%22%3A%22foreground%22%2C%22include_tweet_quick_promote_eligibility%22%3Afalse%2C%22include_professional%22%3Afalse%2C%22skip_author_community_relationship%22%3Afalse%2C%22include_conversation_context%22%3Afalse%2C%22include_is_member%22%3Afalse%2C%22autoplay_enabled%22%3Atrue%2C%22cursor%22%3A%22DAABCgABFzZgmfsAJxEIAAMAAAABAAA%22%2C%22include_reply_device_follow%22%3Afalse%2C%22display_size%22%3A%7B%22width%22%3A640%2C%22height%22%3A1136%7D%2C%22include_dm_muting%22%3Afalse%2C%22is_member_target_user_id%22%3A%220%22%2C%22include_unmention_info_override%22%3Afalse%7D"
    payload = {'grant_type': 'client_credentials'}
    response = requests.request("GET", url, headers=req_headers, data=payload)

    print(response.text)


