import time
import random
import hashlib
import hmac
import base64
import urllib.parse



def generate_oauth_signature(consumer_key, consumer_secret):
    oauth_signature_method = 'HMAC-SHA1'
    oauth_timestamp = str(int(time.time()))
    oauth_version = '1.0'

    # Generate a random string for the nonce
    oauth_nonce = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(32))

    # Prepare the base string
    base_string = '&'.join([
        'oauth_consumer_key=' + consumer_key,
        'oauth_nonce=' + oauth_nonce,
        'oauth_signature_method=' + oauth_signature_method,
        'oauth_timestamp=' + oauth_timestamp,
        'oauth_version=' + oauth_version
    ])

    # Generate the signature key
    signature_key = consumer_secret + '&'

    # Calculate the signature
    signature = base64.b64encode(hmac.new(signature_key.encode('utf-8'), base_string.encode('utf-8'), hashlib.sha1).digest())

    return oauth_signature_method, oauth_timestamp, oauth_version, signature.decode('utf-8'), oauth_nonce

# Example usage
consumer_key = '3rJOl1ODzm9yZy63FACdg'
consumer_secret = '5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8'
oauth_signature_method, oauth_timestamp, oauth_version, oauth_signature, oauth_nonce = generate_oauth_signature(consumer_key, consumer_secret)

encoded_signature = urllib.parse.quote(oauth_signature)

print("OAuth Consumer Key: ", consumer_key)
print("OAuth Signature Method:", oauth_signature_method)
print("OAuth Timestamp:", oauth_timestamp)
print("OAuth Version:", oauth_version)
print("OAuth nonce:", oauth_nonce)
print("OAuth version:", oauth_version)
print("OAuth Signature:", oauth_signature)
print("OAuth Signature:", encoded_signature)

auth = 'OAuth oauth_consumer_key="{consumer_key}",oauth_signature_method="HMAC-SHA1",oauth_timestamp="{oauth_timestamp}",oauth_nonce="{oauth_nonce}",oauth_version="1.0",oauth_signature="{encoded_signature}"'

print(str(auth))

import requests

url = "https://api.twitter.com/graphql/TFwspiiwvDFwJDqgs6-Bcw/SearchTimeline"

payload = {}
headers = {
  'Authorization': auth,
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
