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


import hashlib
import hmac
import urllib
from random import getrandbits


class OAuthSignature():

    # Twitter API url
    url = ""

    # User secret keys
    secrets = {
        'consumer_secret': "",
        'token_secret': ""
    }

    def generate(self, params):
        """
        Generate Twitter signature
        """

        # Step 1. Collecting parameters
        params_str = '&'.join(
            [('%s=%s' % (self.encode(str(k)), self.encode(str(params[k])))) for k in sorted(params)])

        # Step 2. Creating the signature base string
        # Join the entire message together per the OAuth specification.
        message = "&".join(
            [self.encode("GET"), self.encode(self.url), self.encode(params_str)])

        # Step 3. Getting a signing key
        # consumer secret key
        cSecret = self.encode(self.secrets.get('consumer_secret'))

        # token secret key
        tSecret = self.encode(self.secrets.get('token_secret'))

        # The signing key is simply the percent encoded consumer secret,
        # followed by an ampersand character,
        # followed by the percent encoded token secret
        key = "%s&%s" % (cSecret, tSecret)

        # Step 4. Calculating the signature
        # Create a HMAC-SHA1 signature of the message.
        signature = hmac.new(key, message, hashlib.sha1).digest()

        digestBase64 = signature.encode("base64").rstrip('\n')

        return digestBase64

    def nonce(self):
        """ Generate random nonce value"""
        return str(getrandbits(64))

    def encode(self, text):
        return urllib.quote(str(text), "")

    
request_token_url = "https://api.twitter.com/oauth/request_token"

keys_and_secrets = [
    ("3rJOl1ODzm9yZy63FACdg", "5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8", "Mac")
]

def get_bearer_token():

    url = "https://api.twitter.com/1.1/guest/activate.json"

    payload = {}
    headers = {
      'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text



for consumer_key, consumer_secret, name in keys_and_secrets:

    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    fetch_response = oauth.fetch_request_token(request_token_url)
    print(f"Fetch request token succeeded for {name}!")
    oauth_timestamp = int(time.time())
    oauth_nonce = uuid.uuid4()
    guest_token = json.loads(get_bearer_token())["guest_token"]

    request_url = "https://api.twitter.com/graphql/TFwspiiwvDFwJDqgs6-Bcw/SearchTimeline?features=%7B%22graphql_unified_card_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22unified_cards_ad_metadata_container_dynamic_card_content_query_enabled%22%3Atrue%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22trusted_friends_api_enabled%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Afalse%2C%22tweet_with_visibility_results_prefer_gql_tweet_interstitials_enabled%22%3Atrue%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Afalse%2C%22profile_foundations_has_spaces_graphql_enabled%22%3Afalse%2C%22ios_notifications_replies_mentions_device_follow_enabled%22%3Atrue%2C%22birdwatch_consumption_enabled%22%3Afalse%2C%22rito_safety_mode_features_enabled%22%3Afalse%2C%22tweet_awards_tweet_api_enabled%22%3Afalse%2C%22tweet_with_visibility_results_prefer_gql_soft_interventions_enabled%22%3Atrue%7D&variables=%7B%22include_community_tweet_relationship%22%3Afalse%2C%22raw_query%22%3A%22test%22%2C%22product%22%3A%22Top%22%2C%22include_tweet_quick_promote_eligibility%22%3Afalse%2C%22include_professional%22%3Afalse%2C%22include_conversation_context%22%3Afalse%2C%22skip_author_community_relationship%22%3Afalse%2C%22include_is_member%22%3Afalse%2C%22include_reply_device_follow%22%3Afalse%2C%22include_unmention_info_override%22%3Afalse%2C%22include_dm_muting%22%3Afalse%2C%22query_source%22%3A%22typed_query%22%2C%22is_member_target_user_id%22%3A%220%22%7D"

  
    print("oauth_nonce, " + str(oauth_nonce))
    print("oauth_timestamp, " + str(oauth_timestamp))
    print("oauth_consumer_key, 3rJOl1ODzm9yZy63FACdg")
    print("oauth_consumer_secret, 5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8")
    print("oauth_token, " + str(guest_token) + "-" + str(fetch_response["oauth_token"]))
    print("oauth_token_secret, " + str(fetch_response["oauth_token_secret"]))
    print("oauth_version, 1.0")
    print("oauth_signature_method, HMAC-SHA1")




    oauthCtrl = OAuthSignature()
    oauthCtrl.url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    oauthCtrl.secrets = {
        'consumer_secret': "1234567890",
        'token_secret': '0987654321'
    }

    params = {
        'oauth_version': '1.0',
        'oauth_consumer_key': "3rJOl1ODzm9yZy63FACdg",
        'oauth_token': str(guest_token) + "-" + str(fetch_response["oauth_token"]),
        'oauth_timestamp': str(oauth_timestamp),
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_nonce': str(oauth_nonce)
    }

    print(oauthCtrl.generate(params))

    


#{'oauth_token': '9K0ioQAAAAAACIKFAAABiO6J6bk', 'oauth_token_secret': 'WTpZiNkOWbsROF3XjpjDTwd5cdKts6bf', 'oauth_callback_confirmed': 'true'}
