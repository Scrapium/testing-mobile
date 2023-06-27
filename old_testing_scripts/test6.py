import time
import uuid
from requests_oauthlib import OAuth1Session
import urllib
import hmac
import hashlib
from base64 import b64encode
import urllib
import requests
import json
from collections import OrderedDict

import hashlib
import hmac
import urllib
from random import getrandbits
from urllib.parse import urlparse, parse_qs, quote


def percent_encode(s):
    return urllib.parse.quote(s, safe='~').replace('!', '%21').replace('*', '%2A').replace('\'', '%27').replace('(', '%28').replace(')', '%29')

def hmac_sha1(key, message):
    return b64encode(hmac.new(key.encode(), message.encode(), digestmod=hashlib.sha1).digest())

def merge_dicts(d1, d2):
    d = d1.copy()
    d.update(d2)
    return d

def gen_sorted_param_str(params, key, token, timestamp, nonce, bearer_token):
    param_obj = merge_dicts(
        {
            'oauth_nonce' : nonce,
            'oauth_timestamp' : timestamp,
            'oauth_consumer_key' : key,
            'oauth_token' : bearer_token + "-" + oauth_token,
            'oauth_version' : '1.0',
            'oauth_signature_method' : 'HMAC-SHA1',
        },
        params
    )

    param_obj = OrderedDict(sorted(param_obj.items()))
    param_str = ''
    for k,v in param_obj.items():
        param_str += '&' + k + '=' + percent_encode(str(v))
    return param_str[1:]  # Removes the leading '&'

def oAuthBaseString(method, url, params, key, token, timestamp, nonce, bearer_token):
    return method + '&' + percent_encode(url) + '&' + percent_encode(gen_sorted_param_str(params, key, token, timestamp, nonce, bearer_token))

def oAuthSigningKey(consumer_secret, token_secret):
    return consumer_secret + '&' + token_secret

def oAuthSignature(base_string, signing_key):
    signature = hmac_sha1(signing_key, base_string)
    return percent_encode(signature.decode())





    
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

def get_bearer_token():

    url = "https://api.twitter.com/1.1/guest/activate.json"
    headers = { 'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA' }

    response = requests.request("POST", url, headers=headers, data={})

    return json.loads(response.text)["guest_token"]

def format_oauth_params(params):
    formatted_params = []
    for key, value in params.items():
        formatted_params.append(f'{key}="{value}"')
    return ', '.join(formatted_params)

    
for oauth_consumer_key, oauth_consumer_secret, name in keys_and_secrets:
    print("\n", oauth_consumer_key, oauth_consumer_secret, name, "\n")
    try:
        oauth = OAuth1Session(oauth_consumer_key, client_secret=oauth_consumer_secret).fetch_request_token(request_token_url)

        oauth_token = oauth["oauth_token"]
        oauth_token_secret = oauth["oauth_token_secret"]

        oauth_timestamp = int(time.time())
        oauth_nonce = str(uuid.uuid4()).upper()


        bearer_token = get_bearer_token()


        ###

        url = "https://api.twitter.com/graphql/TFwspiiwvDFwJDqgs6-Bcw/SearchTimeline?features=%7B%22graphql_unified_card_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22unified_cards_ad_metadata_container_dynamic_card_content_query_enabled%22%3Atrue%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22trusted_friends_api_enabled%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Afalse%2C%22tweet_with_visibility_results_prefer_gql_tweet_interstitials_enabled%22%3Atrue%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Afalse%2C%22profile_foundations_has_spaces_graphql_enabled%22%3Afalse%2C%22ios_notifications_replies_mentions_device_follow_enabled%22%3Atrue%2C%22birdwatch_consumption_enabled%22%3Afalse%2C%22rito_safety_mode_features_enabled%22%3Afalse%2C%22tweet_awards_tweet_api_enabled%22%3Afalse%2C%22tweet_with_visibility_results_prefer_gql_soft_interventions_enabled%22%3Atrue%7D&variables=%7B%22include_community_tweet_relationship%22%3Afalse%2C%22raw_query%22%3A%22test%22%2C%22product%22%3A%22Top%22%2C%22include_tweet_quick_promote_eligibility%22%3Afalse%2C%22include_professional%22%3Afalse%2C%22include_conversation_context%22%3Afalse%2C%22skip_author_community_relationship%22%3Afalse%2C%22include_is_member%22%3Afalse%2C%22include_reply_device_follow%22%3Afalse%2C%22include_unmention_info_override%22%3Afalse%2C%22include_dm_muting%22%3Afalse%2C%22query_source%22%3A%22typed_query%22%2C%22is_member_target_user_id%22%3A%220%22%7D"

        # Parse the URL
        parsed_url = urlparse(url)

        # Get the base URL (without query parameters)
        base_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path

        # Extract the query parameters
        params = parse_qs(parsed_url.query)

        # Decode the JSON parameters
        params["features"] = json.loads(urllib.parse.unquote(params["features"][0]))
        params["variables"] = json.loads(urllib.parse.unquote(params["variables"][0]))



        ###


        base_string = oAuthBaseString("GET", "https://api.twitter.com/graphql/TFwspiiwvDFwJDqgs6-Bcw/SearchTimeline", params, oauth_consumer_key, oauth_token, oauth_timestamp, oauth_nonce, bearer_token);
        signing_key = oAuthSigningKey(oauth_consumer_key, oauth_token_secret)

        signature = oAuthSignature(base_string, signing_key)


        #########################

        param_obj = {
            'OAuth oauth_signature': signature,
            'oauth_nonce' : oauth_nonce,
            'oauth_timestamp' : oauth_timestamp,
            'oauth_consumer_key' : oauth_consumer_key,
            'oauth_token' : bearer_token + "-" + oauth_token,
            'oauth_version' : '1.0',
            'oauth_signature_method' : 'HMAC-SHA1',
        }   
        

        param_obj = OrderedDict(sorted(param_obj.items()))

        authorisation = format_oauth_params(param_obj)

        #########################


        #####

        payload = {}
        headers = {
          'Authorization': authorisation,
        }

        for key, value in headers.items():
            print(f'{key}: {value}')


        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)


        #####
        
        """
            oauth_signature
            [v] oauth_nonce
            [v] oauth_timestamp
            
            [v] oauth_consumer_key = "IQKbtAYlXLripLGPWd0HUA"
            [v] oauth_consumer_secret* = "GgDYlkSvaPxGxC4X8liwpUoqKwwr3lCADbz8A7ADU"
            [v] oauth_token
            [v] oauth_version = 1.0
            [v] oauth_signature_method = "HMAC-SHA1"
        """
    except Exception as e:
        print(e)
        pass
