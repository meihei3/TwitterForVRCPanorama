import io
import re
from enum import Enum

import os
import regex
import requests
import tweepy
from PIL import ImageFont, ImageDraw, Image

from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_SECRET, ACCESS_TOKEN

TEXT_IMG_DIR = "./text/"

ASCII_CHARACTER = re.compile("[ -~]")
JPCHAR = "〜～ー＠＃＄％＾＆＊（）｛｝「」＜＞｜￥・！？｀、。＝＋＿ω"
JAPANESE_CHARACTER = regex.compile("[\p{Hiragana}\p{Katakana}\p{Han}%s]" % JPCHAR)

FONT_SIZE = 17
FONT_DIR = "static/fonts/"
IPAEXG_FONT = ImageFont.truetype(FONT_DIR+"ipaexg.ttf", FONT_SIZE)
SYMBOLA_FONT = ImageFont.truetype(FONT_DIR+"Symbola_hint.ttf", FONT_SIZE)
IPAEXG_FONT_M = ImageFont.truetype(FONT_DIR+"ipaexg.ttf", FONT_SIZE-2)
SYMBOLA_FONT_M = ImageFont.truetype(FONT_DIR+"Symbola_hint.ttf", FONT_SIZE-2)
FONT_COLOR = (0, 0, 0)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


class TextType(Enum):
    ASCII = "ascii"
    JAPANESE = "japanese"
    OTHER = "other"


def is_ascii_character(w):
    """
    :param w: character
    :return: boolean
    """
    if len(w) != 1:
        raise ValueError("１文字のみに対応")
    return re.match(ASCII_CHARACTER, w)


def is_japanese(w):
    """
    :param w: character
    :return: boolean
    """
    if len(w) != 1:
        raise ValueError("１文字のみに対応")
    return regex.match(JAPANESE_CHARACTER, w)


def is_nl(w):
    """
    :param w: character
    :return: boolean
    """
    if len(w) != 1:
        raise ValueError("１文字のみに対応")
    return w == "\n"


def add_value(stack, value, _type, clen):
    """
    :param stack:
    :param value:
    :param _type:
    :return:
    """
    if len(stack) == 0 or stack[-1]["type"] != _type:
        stack.append({"type": _type, "data": value, "size": clen})
    else:
        stack[-1]["data"] += value
        stack[-1]["size"] += clen


def parse_text(text, wrap=16):
    width = 0
    parsed_text = [[]]
    for w in text:
        line = parsed_text[-1]
        if is_ascii_character(w):
            add_value(line, w, TextType.ASCII, 0.5)
            width += 0.5
        elif is_japanese(w):
            add_value(line, w, TextType.JAPANESE, 1)
            width += 1
        elif is_nl(w):
            parsed_text.append([])
            width = 0
        else:
            add_value(line, w, TextType.OTHER, 1)
            width += 1
        if width >= wrap:
            parsed_text.append([])
            width = 0
    return parsed_text


def create_text_image(draw, text, offset=(6, 76), wrap=16, font_color=FONT_COLOR, font_size=FONT_SIZE,
                      text_font=IPAEXG_FONT, text_emoji_font=SYMBOLA_FONT):
    """
    :param draw: ImageDrawインスタンス
    :param text: tweetのメインのtext
    :param offset: textが置かれる場所のオフセット
    :param wrap: なん文字で折り返すか
    :return:
    """
    for i, line in enumerate(parse_text(text, wrap)):
        width = 0
        for part in line:
            x, y = offset[0] + width * font_size, offset[1] + i * font_size
            if part["type"] in (TextType.ASCII, TextType.JAPANESE):
                draw.text((x, y), part["data"], fill=font_color, font=text_font)
            else:
                draw.text((x, y), part["data"], fill=font_color, font=text_emoji_font)
            width += part["size"]


def create_tweet_text(tweet_id):
    """
    create 300x300 image from tweet

    :param tweet_id: (str) tweet id
    :return: None
    """
    # get tweet data
    tweet = api.get_status(str(tweet_id))
    user_name, user_id, user_img_url = tweet.user.name, tweet.user.screen_name, tweet.user.profile_image_url
    text = tweet.text

    # -- create image --
    im = Image.new("RGB", (300, 300), "white")
    # profile image
    im.paste(Image.open(io.BytesIO(requests.get(user_img_url).content)), (6, 6))

    draw = ImageDraw.Draw(im)
    # user name
    draw.text((66, 6), user_name, fill=(0, 0, 0), font=ImageFont.truetype(FONT_DIR+"ipaexg.ttf", 20))
    # screen name
    draw.text((66, 36), '@'+user_id, fill=(30, 30, 30), font=ImageFont.truetype(FONT_DIR+"ipaexg.ttf", 15))
    # tweet text
    create_text_image(draw, text)

    # save
    if not os.path.exists(TEXT_IMG_DIR):
        os.mkdir(TEXT_IMG_DIR)
    im.save(TEXT_IMG_DIR + tweet_id + ".jpg")


def create_timeline_tweet_text(tweet_id):
    # get tweet data
    tweet = api.get_status(str(tweet_id))
    user_name, user_id, user_img_url = tweet.user.name, tweet.user.screen_name, tweet.user.profile_image_url
    text = tweet.text

    # -- create image --
    im = Image.new("RGB", (400, 100), "white")
    # profile image
    im.paste(Image.open(io.BytesIO(requests.get(user_img_url).content)), (6, 6))

    draw = ImageDraw.Draw(im)
    # user name
    draw.text((66, 6), user_name, fill=(0, 0, 0), font=ImageFont.truetype(FONT_DIR+"ipaexg.ttf", 15))

    # tweet text
    create_text_image(draw, text, offset=(66, 36), wrap=21, font_size=15,
                      text_font=IPAEXG_FONT_M, text_emoji_font=SYMBOLA_FONT_M)

    # save
    if not os.path.exists(TEXT_IMG_DIR):
        os.mkdir(TEXT_IMG_DIR)
    im.save(TEXT_IMG_DIR + tweet_id + ".jpg")


if __name__ == '__main__':
    create_timeline_tweet_text("1093111698297282561")
