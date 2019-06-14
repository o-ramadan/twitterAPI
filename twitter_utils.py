import oauth2
import constants
import urllib.parse as urlparse

consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)


def get_request_token():
    # client is used to make requests from API
    # Creates a client for our app (identified by consumer)
    # Use the client to perform a request for the request token
    client = oauth2.Client(consumer)

    # 1st Arg contains URL we want to request
    # We first request the REQUEST_TOKEN_URL
    # 2nd arg is type of url (verb) obtained from twitter documentation
    # in this case POST body is empty
    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
    if response.status != 200:
        print("An error occurred while getting the request token from twitter")

    # Get the request token by parsing the query string returned
    return dict(urlparse.parse_qsl(content.decode('utf-8')))

def get_oauth_verifier(request_token):
    # Ask the user to authorize our app and give us the PIN code
    print("Go to the following website in your browser:")
    print("{}?oauth_token={}".format(constants.AUTHORIZATION_URL, request_token['oauth_token']))

    return input("What is the PIN?")

def get_access_token(request_token, oauth_verifier):
    #Create a Token object which contains the request token and verifier
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)

    #Create a client with our consumer (our app) and the newly created (and verified) token
    client = oauth2.Client(consumer, token)

    #Ask Twitter for an access token, and Twitter knows it should give us it because
    #we've verified the request token
    response, content = client.request(constants.ACCESS_TOKEN_URL,'POST')
    return dict(urlparse.parse_qsl(content.decode('utf-8')))
