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
url = 'https://api.twitter.com/graphql/TFwspiiwvDFwJDqgs6-Bcw/SearchTimeline?features=%7B%22graphql_unified_card_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled'

# Print variables
print('consumer_key:', consumer_key)
print('consumer_secret:', consumer_secret)
print('url:', url)

# Parse URL and parameters
url_parts = urlsplit(url)
base_url = url_parts.scheme + '://' + url_parts.netloc + url_parts.path
params = dict(parse_qsl(url_parts.query))

# Print variables
print('url_parts:', url_parts)
print('base_url:', base_url)
print('params:', params)

# Define headers
headers = {
    'User-Agent': 'Twitter-iPhone/9.63 iOS/15.7.6 (Apple;iPhone8,4;;;;;1;2015)',
}

# Print variable
print('headers:', headers)

# Parameters required for OAuth
oauth_params = {
    'oauth_consumer_key': consumer_key,
    'oauth_nonce':'test', # hashlib.sha1(str(time.time()).encode('utf-8')).hexdigest(),
    'oauth_signature_method': 'HMAC-SHA1',
    'oauth_timestamp': str(1688055990),
    'oauth_version': '1.0'
}

# Print variable
print('oauth_params:', oauth_params)

# Merge all parameters and sort them
all_params = OrderedDict(sorted({**params, **oauth_params}.items()))

# Print variable
print('all_params:', all_params)

# Prepare string to sign
base_string_parts = {
    'method': 'GET',
    'url': base_url,
    'params': urlencode(all_params),
}

# Print variable
print('base_string_parts:', base_string_parts)

base_string = '&'.join([quote_plus(v) for v in base_string_parts.values()])

# Print variable
print('base_string:', base_string)

# Calculate the signature
signing_key = '&'.join([quote_plus(consumer_secret), ''])
signature = base64.b64encode(hmac.new(signing_key.encode('utf-8'), base_string.encode('utf-8'), hashlib.sha1).digest())

# Print variables
print('signing_key:', signing_key)
print('signature:', signature)

# Add the signature to the OAuth parameters
oauth_params['oauth_signature'] = signature.decode('utf-8')

# Print variable
print('oauth_params with signature:', oauth_params)

# Include OAuth parameters to the headers
auth_header = 'OAuth ' + ', '.join(['{}="{}"'.format(quote_plus(k), quote_plus(v)) for k, v in oauth_params.items()])
headers['Authorization'] = auth_header

# Print variable
print('headers with Authorization:', headers)

# Create final URL
final_url = urlunsplit((url_parts.scheme, url_parts.netloc, url_parts.path, urlencode(params), url_parts.fragment))

# Print variable
print('final_url:', final_url)

# Send the request
response = requests.get(final_url, headers=headers)

# Print variable
print('response:', response)

# Handle the response
if response.status_code == 200:
    print('Request was successful')
    data = response.text
    print('response text:', data)
else:
    print('Request failed with status code', response.status_code)
    print('response text:', response.text)