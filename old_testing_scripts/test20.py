import requests
import hmac
import hashlib
import time
import urllib.parse
import base64
import uuid
import json
from requests_oauthlib import OAuth1Session


def get_guest_token():
    url = "https://api.twitter.com/1.1/guest/activate.json"
    headers = {
        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
    }
    response = requests.request("POST", url, headers=headers)
    return json.loads(response.text)["guest_token"]


def generate_oauth_signature(url, method, params, consumer_secret, token_secret):
    base_string = "&".join([method.upper(), urllib.parse.quote(url, safe=''), urllib.parse.quote(params, safe='')])

    key = "&".join([urllib.parse.quote(consumer_secret, safe=''), urllib.parse.quote(token_secret, safe='')])

    signature = base64.b64encode(hmac.new(key.encode('utf-8'), base_string.encode('utf-8'), hashlib.sha1).digest()).decode('utf-8')

    return urllib.parse.quote(signature, safe='')


url = "https://api.twitter.com/graphql/pAyVFRiMFMp9KCfffF7LHg/HomeLatestTimeline"




# Your provided credentials
oauth_consumer_key = "3rJOl1ODzm9yZy63FACdg"
oauth_consumer_secret = "5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8"
oauth = OAuth1Session(oauth_consumer_key, client_secret=oauth_consumer_secret).fetch_request_token("https://api.twitter.com/oauth/request_token")

oauth_token = oauth["oauth_token"]
oauth_token_secret = oauth["oauth_token_secret"]

# Nonce and timestamp
oauth_nonce = str(uuid.uuid4()).replace("-", "")
oauth_timestamp = str(int(time.time()))  # Current time

# Generate guest token
guest_token = get_guest_token()
print("Guest Token:", guest_token)

# Construct the OAuth token
#oauth_token = f"{guest_token}-{oauth_token}"
#print("OAuth Token:", oauth_token)

# Prepare the parameters
parameters = {
    'grant_type': 'client_credentials',
    'features': json.dumps({
        "graphql_unified_card_enabled": True,
        "tweetypie_unmention_optimization_enabled": True,
        "view_counts_everywhere_api_enabled": True,
        "unified_cards_ad_metadata_container_dynamic_card_content_query_enabled": True,
        "freedom_of_speech_not_reach_fetch_enabled": True,
        "trusted_friends_api_enabled": True,
        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": False,
        "birdwatch_consumption_enabled": False,
        "tweet_with_visibility_results_prefer_gql_tweet_interstitials_enabled": True,
        "profile_foundations_has_spaces_graphql_enabled": False,
        "c9s_tweet_anatomy_moderator_badge_enabled": False,
        "rito_safety_mode_features_enabled": False,
        "tweet_awards_tweet_api_enabled": False,
        "ios_notifications_replies_mentions_device_follow_enabled": True,
        "tweet_with_visibility_results_prefer_gql_soft_interventions_enabled": True
    }),
    'variables': json.dumps({
        "latest_control_available": True,
        "include_community_tweet_relationship": False,
        "request_context": "foreground",
        "include_tweet_quick_promote_eligibility": False,
        "include_professional": False,
        "skip_author_community_relationship": False,
        "include_conversation_context": False,
        "include_is_member": False,
        "autoplay_enabled": True,
        "cursor": "DAABCgABFzZgmfsAJxEIAAMAAAABAAA",
        "include_reply_device_follow": False,
        "display_size": {"width": 640, "height": 1136},
        "include_dm_muting": False,
        "is_member_target_user_id": "0",
        "include_unmention_info_override": False
    })
}

# Sort and encode the parameters
sorted_parameters = sorted(parameters.items(), key=lambda x: x[0])
encoded_parameters = urllib.parse.urlencode(sorted_parameters)

# Prepare the signature base string
base_string = f"GET&{urllib.parse.quote(url, safe='')}&{urllib.parse.quote(encoded_parameters, safe='')}"
print("Base String:", base_string)

# Generate the OAuth signature
oauth_signature = generate_oauth_signature(url, "GET", base_string, oauth_consumer_secret, oauth_token_secret)
print("OAuth Signature:", oauth_signature)

# Prepare the headers-
headers = {
#    'Authorization': f'OAuth oauth_consumer_key="{oauth_consumer_key}", oauth_signature_method="HMAC-SHA1", oauth_signature="{oauth_signature}", oauth_timestamp="{oauth_timestamp}", oauth_nonce="{oauth_nonce}", oauth_version="1.0"'
    'Authorization': f'OAuth oauth_consumer_key="{oauth_consumer_key}",oauth_signature_method="HMAC-SHA1",oauth_timestamp="{oauth_timestamp}",oauth_nonce="{oauth_nonce}",oauth_version="1.0",oauth_signature="{oauth_signature}"'
}
print("Headers:", headers)

# Make the API request
response = requests.get(url, headers=headers, params=parameters, data={'grant_type': 'client_credentials'})
print(response.text)

"""
[v]    OAuth oauth_consumer_key="3rJOl1ODzm9yZy63FACdg",
[v]    oauth_signature_method="HMAC-SHA1",
[v]   oauth_timestamp="1687808706",
[v]   oauth_nonce="J2ztERD333f",
[v]    oauth_version="1.0",
[v]    oauth_signature="vBagrkJ1LMJqDs8hO04hraSB9s4%3D"
"""