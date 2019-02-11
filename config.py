from PIL import ImageFont
import re
import regex


class FontData:
    def __init__(self, font, color):
        self.FONT = font
        self.SIZE = font.size
        self.COLOR = color


# dirs
TEXT_STATUS_IMG_DIR = "./text/status/"
TEXT_TIMELINE_IMG_DIR = "./text/timeline/"
FONT_DIR = "static/fonts/"
IMAGE_DIR = "static/img/"

# filename
TMP_FILE = "timeline.tmp"

# regex
ASCII_CHARACTER = re.compile("[ -~]")
JPCHAR = "〜～ー＠＃＄％＾＆＊（）｛｝「」＜＞｜￥・！？｀、。＝＋＿ω"
JAPANESE_CHARACTER = regex.compile("[\p{Hiragana}\p{Katakana}\p{Han}%s]" % JPCHAR)

# font
USER_NAME_FONT = FontData(font=ImageFont.truetype(FONT_DIR+"ipaexg.ttf", 20), color=(0, 0, 0))
USER_NAME_FONT_M = FontData(font=ImageFont.truetype(FONT_DIR+"ipaexg.ttf", 15), color=(0, 0, 0))
SCREEN_NAME_FONT = FontData(font=ImageFont.truetype(FONT_DIR+"ipaexg.ttf", 15), color=(30, 30, 30))
TWEET_IPAEXG_FONT = FontData(font=ImageFont.truetype(FONT_DIR+"ipaexg.ttf", 17), color=(0, 0, 0))
TWEET_IPAEXG_FONT_M = FontData(font=ImageFont.truetype(FONT_DIR+"ipaexg.ttf", 17), color=(0, 0, 0))
TWEET_SYMBOLA_FONT = FontData(font=ImageFont.truetype(FONT_DIR+"Symbola_hint.ttf", 15), color=(0, 0, 0))
TWEET_SYMBOLA_FONT_M = FontData(font=ImageFont.truetype(FONT_DIR+"Symbola_hint.ttf", 15), color=(0, 0, 0))
