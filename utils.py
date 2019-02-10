import pickle as pk


def get_tweet_id(filename: str, idx: int):
    with open(filename, 'rb') as f:
        return pk.load(f)[idx]
