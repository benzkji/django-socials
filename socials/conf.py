import sys

from django.conf import settings

from socials.utils import check_settings

# globals
ENABLE_TAGS = False  # parse hashtags?
DATE_FORMAT = "%d.%m.%Y"  # output date format
LOCAL_IMAGES = True  # save images to local media folder
DEBUG = False

# insta
INSTAGRAM_API = "https://graph.instagram.com/"
INSTAGRAM_URL = "https://www.instagram.com/"
INSTAGRAM_TITLE_TRUNCATE = 60
# not yet?! INSTAGRAM_REFRESH_TOKEN_BEFORE_EXPIRE = 1209600  # 14 days

# fb

# tweetie


check_settings("SOCIALS", sys.modules[__name__], settings)
