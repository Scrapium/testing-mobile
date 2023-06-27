import requests
import time
import urllib

# generate_signature

oauth_consumer_key = "3rJOl1ODzm9yZy63FACdg"
oauth_consumer_secret = "5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8"


def enc(text):
    return urllib.parse.quote(text, safe='')

def sign_request(oauth_token_secret,raw):
    # key = b"CONSUMER_SECRET&oauth_token_secret" #
    key = b"GgDYlkSvaPxGxC4X8liwpUoqKwwr3lCADbz8A7ADU&"+oauth_token_secret.encode()

    hashed = hmac.new(key, raw, hashlib.sha1)

    # The signature
    return base64.b64encode(hashed.digest())






time1 = str(int(time.time()))

testurl = "https://api.twitter.com/graphql/TFwspiiwvDFwJDqgs6-Bcw/SearchTimeline"

oauth_consumer_key = "IQKbtAYlXLripLGPWd0HUA"
oauth_nonce = "1A195122-682C-447F-9D1F-964D0DEDFEE8"
oauth_timestamp = "1687645082"
oauth_token = "1672630233671823361-iOiY4xgK8K3oG2rl4QevBOWktkCXPI"


databeforeEnc = enc("GET&" + str(testurl) + "&oauth_consumer_key={}&oauth_nonce={}&oauth_signature_method=HMAC-SHA1&oauth_timestamp={}&oauth_token={}&oauth_version=1.0".format(
        oauth_consumer_key, oauth_nonce, oauth_timestamp, oauth_token))
sig = sign_request(oauth_token_secret,databeforeEnc.encode()).decode().replace("=", "%3D")


print(sig)

#headers = {
#        'Connection': 'close', 'X-Twitter-Client-Language': 'en',
#           'Content-Type': 'application/x-www-form-urlencoded', 'Host': 'api.twitter.com',
#           'Authorization': 'OAuth oauth_signature="{}", oauth_nonce="133333333337", oauth_timestamp="{}", oauth_consumer_key="IQKbtAYlXLripLGPWd0HUA", oauth_token="{}", oauth_version="1.0", oauth_signature_method="HMAC-SHA1"'.format(
#               sig,time1, oauth_token)}




#req1 = requests.post("https://api.twitter.com/1.1/statuses/destroy/"+ids+".json", headers=headers)
