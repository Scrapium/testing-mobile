import requests
import json
import hmac
import hashlib
import base64
import time
from urllib.parse import quote_plus, urlencode, parse_qsl, urlsplit, urlunsplit
from collections import OrderedDict

# Define the consumer key, consumer secret, and API endpoint
consumer_key = '3rJOl1ODzm9yZy63FACdg'
consumer_secret = '5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8'
url = 'https://api.twitter.com/graphql/TFwspiiwvDFwJDqgs6-Bcw/SearchTimeline?features=%7B%22graphql_unified_card_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22unified_cards_ad_metadata_container_dynamic_card_content_query_enabled%22%3Atrue%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22trusted_friends_api_enabled%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Afalse%2C%22tweet_with_visibility_results_prefer_gql_tweet_interstitials_enabled%22%3Atrue%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Afalse%2C%22profile_foundations_has_spaces_graphql_enabled%22%3Afalse%2C%22ios_notifications_replies_mentions_device_follow_enabled%22%3Atrue%2C%22birdwatch_consumption_enabled%22%3Afalse%2C%22rito_safety_mode_features_enabled%22%3Afalse%2C%22tweet_awards_tweet_api_enabled%22%3Afalse%2C%22tweet_with_visibility_results_prefer_gql_soft_interventions_enabled%22%3Atrue%7D&variables=%7B%22include_community_tweet_relationship%22%3Afalse%2C%22raw_query%22%3A%22test%22%2C%22product%22%3A%22Top%22%2C%22include_tweet_quick_promote_eligibility%22%3Afalse%2C%22include_professional%22%3Afalse%2C%22include_conversation_context%22%3Afalse%2C%22skip_author_community_relationship%22%3Afalse%2C%22include_is_member%22%3Afalse%2C%22include_reply_device_follow%22%3Afalse%2C%22include_unmention_info_override%22%3Afalse%2C%22include_dm_muting%22%3Afalse%2C%22query_source%22%3A%22typed_query%22%2C%22is_member_target_user_id%22%3A%220%22%7D'

# Parse URL and parameters
url_parts = urlsplit(url)
base_url = url_parts.scheme + '://' + url_parts.netloc + url_parts.path
params = dict(parse_qsl(url_parts.query))

# Define headers
headers = {
    'User-Agent': 'Twitter-iPhone/9.63 iOS/15.7.6 (Apple;iPhone8,4;;;;;1;2015)',
}

# Parameters required for OAuth
oauth_params = {
    'oauth_consumer_key': consumer_key,
    'oauth_nonce': hashlib.sha1(str(time.time()).encode('utf-8')).hexdigest(),
    'oauth_signature_method': 'HMAC-SHA1',
    'oauth_timestamp': str(int(time.time())),
    'oauth_version': '1.0'
}

# Merge all parameters and sort them
all_params = OrderedDict(sorted({**params, **oauth_params}.items()))

# Prepare string to sign
base_string_parts = {
    'method': 'GET',
    'url': base_url,
    'params': urlencode(all_params),
}

base_string = '&'.join([quote_plus(v) for v in base_string_parts.values()])

# Calculate the signature
signing_key = '&'.join([quote_plus(consumer_secret), ''])
signature = base64.b64encode(hmac.new(signing_key.encode('utf-8'), base_string.encode('utf-8'), hashlib.sha1).digest())

# Add the signature to the OAuth parameters
oauth_params['oauth_signature'] = signature.decode('utf-8')

# Include OAuth parameters to the headers
auth_header = 'OAuth ' + ', '.join(['{}="{}"'.format(quote_plus(k), quote_plus(v)) for k, v in oauth_params.items()])
headers['Authorization'] = auth_header

# Create final URL
final_url = urlunsplit((url_parts.scheme, url_parts.netloc, url_parts.path, urlencode(params), url_parts.fragment))

# Send the request
response = requests.get(final_url, headers=headers)

# Handle the response
if response.status_code == 200:
    print('Request was successful')
    data = json.loads(response.text)
    print(json.dumps(data, indent=4))
else:
    print(response.text)
    print(f'Request failed with status code {response.status_code}')
