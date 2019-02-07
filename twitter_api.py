import tweepy
from functools import lru_cache

from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_SECRET, ACCESS_TOKEN


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


@lru_cache(maxsize=None)
def tweet_from_id(tweet_id: str):
    return api.get_status(str(tweet_id))


def get_tl_id(cnt=10):
    return [tw.id_str for tw in api.home_timeline(count=cnt)]

