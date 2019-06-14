import constants
from user import User
from database import Database
from twitter_utils import get_access_token, get_request_token, get_oauth_verifier

#Allows twitter API to recognize our app using these two unique identifiers
#I am the consumer (creator of app)

Database.initialize(user = 'postgres',
                    password = 'Omar1998',
                    database = 'Learning',
                    host = 'localhost')


email_address = input("Enter your Email: ")
user = User.load_from_db_by_email(email_address)

if not user:
    request_token = get_request_token()

    oauth_verifier = get_oauth_verifier(request_token)

    access_token = get_access_token(request_token,oauth_verifier)

    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name:")

    user = User(email_address, first_name, last_name,
                access_token['oauth_token'], access_token['oauth_token_secret'], None)
    user.save_to_db()

tweets = user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q=salah+filter:videos')

for tweet in tweets['statuses']:
    print(tweet['text'])