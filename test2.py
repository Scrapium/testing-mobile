from requests.auth import HTTPBasicAuth
import requests

def obtain_access_token():

    oauth_version = 2
    app_key = "IQKbtAYlXLripLGPWd0HUA"
    app_secret = "GgDYlkSvaPxGxC4X8liwpUoqKwwr3lCADbz8A7ADU"
    request_token_url = "https://api.twitter.com/oauth/request_token"
    
    """Returns an OAuth 2 access token to make OAuth 2 authenticated
    read-only calls.

    :rtype: string
    """
    if oauth_version != 2:
        raise TwythonError('This method can only be called when your \
                           OAuth version is 2.0.')

    data = {'grant_type': 'client_credentials'}
    basic_auth = HTTPBasicAuth(app_key, app_secret)


    response = requests.post(request_token_url, data=data, auth=basic_auth)
    content = response.content.decode('utf-8')
    try:
        content = content.json()
    except AttributeError:
        print(content)
        content = json.loads(content)
        access_token = content['access_token']


obtain_access_token()
