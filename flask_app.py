import os
from flask import Flask, send_from_directory, abort
import pickle as pk

from tweet_img_generater import create_tweet_text, create_timeline_tweet_text
from twitter_api import get_tl_id

TEXT_STATUS_IMG_DIR = "./text/status/"
TEXT_TIMELINE_IMG_DIR = "./text/timeline/"
TMP_FILE = "timeline.tmp"

app = Flask(__name__)


@app.route('/')
def index():
    return "hello"


@app.route('/api/tweet/<int:idx>')
def tweet(idx):
    if idx not in range(10):
        abort(404)
    with open(TMP_FILE, 'rb') as f:
        tid = pk.load(f)[idx]
    if tid + ".jpg" not in os.listdir(TEXT_STATUS_IMG_DIR):
        create_tweet_text(tid)
    return send_from_directory(TEXT_STATUS_IMG_DIR,  tid + ".jpg")


@app.route('/api/timeline/<int:idx>')
def tl_tweet(idx):
    print(idx)
    if idx not in range(10):
        abort(404)
    with open(TMP_FILE, 'rb') as f:
        tid = pk.load(f)[idx]
    if tid + ".jpg" not in os.listdir(TEXT_TIMELINE_IMG_DIR):
        create_timeline_tweet_text(tid)
    return send_from_directory(TEXT_TIMELINE_IMG_DIR, tid + ".jpg")


@app.route("/api/refresh/")
def refresh():
    ids = get_tl_id()
    with open(TMP_FILE, 'wb') as f:
        pk.dump(ids, f)
    return "ok"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
