import requests
import json
import hmac
import hashlib
import base64
import time
from urllib.parse import quote_plus, urlencode, parse_qsl, urlsplit, urlunsplit
from collections import OrderedDict


import urllib.parse

def dict_to_str(dict_obj):
    # Create a list to store the encoded parts
    encoded_parts = []

    # Loop through the dictionary and convert each dict to JSON string, then quote it
    for key, value in dict_obj.items():
        encoded_value = urllib.parse.quote(json.dumps(value, separators=(',', ':')))
        encoded_parts.append(f'{key}={encoded_value}')

    # Join the parts with '&' and return the result
    return '&'.join(encoded_parts)

def str_to_dict(encoded_str):
    # Split the string into two parts based on '&'
    str_parts = encoded_str.split('&')

    # Create a dictionary to store both parts
    dict_parts = {}

    # Loop through each part and parse the key-value pairs
    for part in str_parts:
        # Split each part into key and value
        key, value = part.split('=')

        # Unquote the value to decode it, and convert the decoded JSON string to Python dict using json.loads
        dict_parts[key] = json.loads(urllib.parse.unquote(value))

    return dict_parts

def twitter(search_string, cursor = False):
    get_parameters = {
        "features": {
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
            "ios_notifications_replies_mentions_device_follow_enabled": False,
            "rito_safety_mode_features_enabled": False,
            "tweet_awards_tweet_api_enabled": False,
            "c9s_tweet_anatomy_moderator_badge_enabled": False,
            "tweet_with_visibility_results_prefer_gql_soft_interventions_enabled": True,
        },
        "variables": {
            "include_community_tweet_relationship": False,
            "include_dm_muting": False,
            "product": "Top",
            "include_tweet_quick_promote_eligibility": False,
            "include_professional": False,
            "skip_author_community_relationship": False,
            "include_is_member": False,
            "include_conversation_context": False,
            "include_reply_device_follow": False,
            "include_unmention_info_override": False,
            "query_source": "typed_query",
            "is_member_target_user_id": "0",
            "raw_query": search_string,
        },
    }

    if(cursor != False):
        get_parameters["variables"]["cursor"] = cursor


    encoded_str = dict_to_str(get_parameters)
    url = 'https://api.twitter.com/graphql/TFwspiiwvDFwJDqgs6-Bcw/SearchTimeline?' + str(encoded_str)


    # Define the consumer key, consumer secret, and API endpoint
    consumer_key = '3rJOl1ODzm9yZy63FACdg'
    consumer_secret = '5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8'


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
        print("\n")
        print('Request was successful')
        data = json.loads(response.text)
        #print(json.dumps(data, indent=4))
        return data
    else:
        print(response.text)
        print(f'Request failed with status code {response.status_code}')
        if(response.status_code == 429 and response.text == "Rate limit exceeded\n"):
            print("RATE LIMIT EXCEEDED")
        return False

cursor = False

i = 0

while True:
    data = twitter("jake", cursor)

    if(data):

        lines = json.dumps(data, indent=4)
        f = open("./samples/"+str(i) + '-request.json', 'w')
        for line in lines:
            f.write(line)
        f.close()
        

        #cursor = data["data"]["search_by_raw_query"]["search_timeline"]["timeline"]["instructions"][0]["entries"][-1]["content"]["value"]
        timeline_entries = data["data"]["search_by_raw_query"]["search_timeline"]["timeline"]["instructions"][0]["entries"]

        for item in timeline_entries:
            entry_type = item["content"]["__typename"]
            
            if(entry_type == "TimelineTimelineModule"):
                #print("> Found timeline module element")
                pass
            elif(entry_type == "TimelineTimelineItem"):
                #print("> Found timeline tweet element")

                # get the tweet text:
                tweet_text = item["content"]["content"]["tweet_results"]["result"]["legacy"]["full_text"]
                #print(tweet_text)

            elif(entry_type == "TimelineTimelineCursor"):
                #print("> Found timeline cursor element")
                cursor_type = item["content"]["cursor_type"]
                if(cursor_type == "Bottom"):
                    print("found bottom element *************")
                    cursor = item["content"]["value"]
                    
            elif(entry_type == "TimelineReplaceEntry"):
                print("found replace entry")

        i += 1