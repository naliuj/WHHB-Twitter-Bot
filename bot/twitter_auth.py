import tweepy
from CONFIG import twitter_auth


def authenticate():
    auth = tweepy.OAuthHandler(twitter_auth['CONSUMER_KEY'], twitter_auth['CONSUMER_SECRET'])
    auth.set_access_token(twitter_auth['ACCESS_TOKEN'], twitter_auth['ACCESS_TOKEN_SECRET'])
    return tweepy.API(auth)
