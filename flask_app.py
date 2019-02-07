from flask import Flask, send_from_directory

from tweet_img_generater import create_tweet_text

TEXT_IMG_DIR = "./text/"

app = Flask(__name__)


@app.route('/')
def index():
    return "hello"


@app.route('/api/tweet/<tid>')
def p(tid):
    create_tweet_text(tid)
    return send_from_directory(TEXT_IMG_DIR,  tid + ".jpg")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
