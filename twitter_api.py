import tweepy
from functools import lru_cache

from keys import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_SECRET, ACCESS_TOKEN


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


@lru_cache(maxsize=None)
def tweet_from_id(tweet_id: str):
    return api.get_status(str(tweet_id))


def get_tl_id(cnt=10):
    return [tw.id_str for tw in api.home_timeline(count=cnt)]


def get_searched_id(trg: str, cnt=10):
    return [tw.id_str for tw in api.search(q="%s -filter:retweets" % trg, lang='ja',
                                         result_type='recent', count=cnt)]


def retweet(tweet_id: str):
    return api.retweet(str(tweet_id))


def favorite(tweet_id: str):
    return api.create_favorite(str(tweet_id))


if __name__ == '__main__':
    # print(retweet("1094863090003304449"))
    # print(favorite("1094863090003304449"))
    pass
