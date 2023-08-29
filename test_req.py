import requests_oauthlib

def test_token(device_type, consumer_key, consumer_secret):
    print("----- DEVICE TYPE: " + device_type + "-----")

    try:
        access_token_url = 'https://api.twitter.com/oauth/request_token'
        oauth = requests_oauthlib.OAuth1Session(consumer_key, client_secret=consumer_secret)
        fetch_response = oauth.fetch_request_token(access_token_url)
        resource_owner_key = fetch_response.get('oauth_token')
        resource_owner_secret = fetch_response.get('oauth_token_secret')
        print("[X] Token Request accepted\n")
        print("oauth_token: " + resource_owner_key + " (" + str(len(resource_owner_key)) + ")")
        print("oauth_secret: " + resource_owner_secret + " (" + str(len(resource_owner_secret)) + ")")
    except requests_oauthlib.oauth1_session.TokenRequestDenied:
        print("[X] Token Request Denied\n")
    


devices = [
    {"name": "Twitter for Android", "type": "PIN", "key": "3nVuSoBZnx6U4vzUxf5w", "secret": "Bcs59EFbbsdF6Sl9Ng71smgStWEGwXXKSjYvPVt7qys"},
    {"name": "Twitter for iPhone", "type": "PIN", "key": "IQKbtAYlXLripLGPWd0HUA", "secret": "GgDYlkSvaPxGxC4X8liwpUoqKwwr3lCADbz8A7ADU"},
    {"name": "Twitter for iPad", "type": "PIN", "key": "CjulERsDeqhhjSme66ECg", "secret": "IQWdVyqFxghAtURHGeGiWAsmCAGmdW3WmbEx6Hck"},
    {"name": "Twitter for Mac", "type": "PIN", "key": "3rJOl1ODzm9yZy63FACdg", "secret": "5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8"},
    {"name": "Twitter for Windows Phone", "type": "PIN", "key": "yN3DUNVO0Me63IAQdhTfCA", "secret": "c768oTKdzAjIYCmpSNIdZbGaG0t6rOhSFQP0S5uC79g"},
    {"name": "Twitter for Google TV", "type": "PIN", "key": "iAtYJ4HpUVfIUoNnif1DA", "secret": "172fOpzuZoYzNYaU3mMYvE8m8MEyLbztOdbrUolU"},
    {"name": "TweetDeck", "type": "CALLBACK", "key": "yT577ApRtZw51q4NPMPPOQ", "secret": "3neq3XqN5fO3obqwZoajavGFCUrC42ZfbrLXy5sCv8"},
    {"name": "Twitter for Windows", "type": "CALLBACK", "key": "TgHNMa7WZE7Cxi1JbkAMQ", "secret": "SHy9mBMBPNj3Y17et9BF4g5XeqS4y3vkeW24PttDcY"},
    {"name": "Twitter for Android Sign-Up", "type": "PIN", "key": "RwYLhxGZpMqsWZENFVw", "secret": "Jk80YVGqc7Iz1IDEjCI6x3ExMSBnGjzBAH6qHcWJlo"},
    {"name": "Tweetbot for iOS", "type": "CALLBACK", "key": "8AeR93em84Pyum5i1QGA", "secret": "ugCImRuw376Y9t9apIq6bgWGNbb1ymBrx2K5NK0ZI"},
    {"name": "YoruFukurou", "type": "CALLBACK", "key": "WfEZ02WzcqZMvs4HJMZLA", "secret": "69zIxwA9KSuY4IDYRT2Bfk1rq62Nq1csspXOfSRKhg"},
    {"name": "HootSuite", "type": "CALLBACK", "key": "w1Gybt9LP9zG46mS1X3UAw", "secret": "hRIK4RWjAO4pokQCvmNCynRAY8Jc8edV1kcV2go6g"},
    {"name": "ShootingStar", "type": "CALLBACK", "key": "Eb8hyAEUju1f2g0i2iSwTQ", "secret": "lOBgiyGJcYK4jsUc2It38ORlsJC0a60USShZrosMTlw"},
    {"name": "ShootingStarPro", "type": "CALLBACK", "key": "I8ye5YHbnFUVzrWdyEkXw", "secret": "UTXlrSs9IuZuhfxfwBDckzMDHCI8HRlTNtitiV2OL4"},
    {"name": "twicca", "type": "PIN", "key": "7S2l5rQTuFCj4YJpF7xuTQ", "secret": "L9VHCXMKBPb2eWjvRvQTOEmOyGlH4W50getaQJPya4"},
    {"name": "Twitcle", "type": "CALLBACK", "key": "lYa4VucwdoUUTQLC2utgtg", "secret": "NfnIALNRMcrvC844yypUubWp2xmuiL3zbLN8osjWntM"},
    {"name": "Echofon", "type": "PIN", "key": "yqoymTNrS9ZDGsBnlFhIuw", "secret": "OMai1whT3sT3XMskI7DZ7xiju5i5rAYJnxSEHaKYvEs"},
    {"name": "Instagram", "type": "PIN", "key": "7YBPrscvh0RIThrWYVeGg", "secret": "sMO1vDyJ9A0xfOE6RyWNjhTUS1sNqsa7Ae14gOZnw"}
]

for device in devices:
    test_token(device["name"], device["key"], device["secret"])