from os import getenv
import not_tweepy as tweepy
from .models import DB, User, Tweet
import spacy

# Get our API keys
key = getenv('TWITTER_API_KEY')
secret = getenv('TWITTER_API_KEY_SECRET')


#connect to twitter API
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)
TWITTER = tweepy.API(TWITTER_AUTH)


def add_update_user(username):
    '''
    take username and pull the user data and tweets from the API.
    If this user is already exists in database we will just check
    to see if there are any new tweets from the user and update
    '''
    try:
        twitter_user = TWITTER.get_user(screen_name=username)

        # is there a user with the same name?
        # if not a new user will be created in DB

        db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, username=username)

        DB.session.add(db_user)

        tweets = twitter_user.timeline(count=200, 
                                        exclude_replies=True,
                                        include_rts=False,
                                        tweet_mode='extended',
                                        since_id=db_user.newest_tweet_id)

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # add tweets

        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, 
                            text=tweet.full_text[:300], 
                            vect=tweet_vector,
                            user_id=db_user.id)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
    except Exception as e:
        print(f"Error processing {username}:{e}")
        raise e

    else:
       #save the changes to the database

        DB.session.commit()

nlp = spacy.load('my_model/')

# function to return word embedding of text
def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector
