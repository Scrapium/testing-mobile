"""
A function for asking the user for their Twitter API keys.
"""

import requests

from requests_oauthlib import OAuth1
from urllib.parse import parse_qs


def test():
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""
    resource_owner_key = ""
    resource_owner_secret = ""

    bearer_token = "AAAAAAAAAAAAAAAAAAAAAAj4AQAAAAAAPraK64zCZ9CSzdLesbE7LB%2Bw4uE%3DVJQREvQNCZJNiz3rHO7lOXlkVOQkzzdsgu6wWgcazdMUaGoUGm"

    consumer_key = "3rJOl1ODzm9yZy63FACdg"
    consumer_secret = "5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8"

    # verify that the keys work to get the bearer token
    url = "https://api.twitter.com/oauth2/token"
    params = {"grant_type": "client_credentials"}
    auth = requests.auth.HTTPBasicAuth(consumer_key, consumer_secret)
    try:
        resp = requests.post(url, params, auth=auth)
        resp.raise_for_status()
        result = resp.json()
        bearer_token = result["access_token"]
        print(result)
    except Exception as e:
        print(e)
        return None



    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1(consumer_key, client_secret=consumer_secret)
    r = requests.post(url=request_token_url, auth=oauth)

    credentials = parse_qs(r.text)
    if not credentials:
        print("\nError: invalid credentials.")
        print(
            "Please check that you are copying and pasting correctly and try again.\n"
        )
        return

    resource_owner_key = credentials.get("oauth_token")[0]
    resource_owner_secret = credentials.get("oauth_token_secret")[0]


    return {
        "consumer_key": consumer_key,
        "consumer_secret": consumer_secret,
        "resource_owner_key": resource_owner_key,
        "resource_owner_secret": resource_owner_secret,
        "bearer_token": bearer_token,
    }

print(test())

"""
x    OAuth oauth_signature="2t2zyhHu%2BfNwHUHKvFmF5D2FMHE%3D", 
x    oauth_nonce="13B231DA-83F5-4ADD-9FA8-9F1C4811BCF2", 
v    oauth_timestamp="1687807722", 
v    oauth_consumer_key="IQKbtAYlXLripLGPWd0HUA", 
v    oauth_token="1673412470965170182-Ep69yeiJSpx5BGRFJkXXMwURLDL6as", 
v    oauth_version="1.0", oauth_signature_method="HMAC-SHA1"
"""

# AAAAAAAAAAAAAAAAAAAAAAj4AQAAAAAAPraK64zCZ9CSzdLesbE7LB%2Bw4uE%3DVJQREvQNCZJNiz3rHO7lOXlkVOQkzzdsgu6wWgcazdMUaGoUGm
# IQKbtAYlXLripLGPWd0HUA
# GgDYlkSvaPxGxC4X8liwpUoqKwwr3lCADbz8A7ADU