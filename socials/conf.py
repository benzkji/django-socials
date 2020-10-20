import sys

from django.conf import settings

from socials.utils import check_settings


# globals
ENABLE_TAGS = False
DATE_FORMAT = '%d.%m.%Y'

# insta
INSTAGRAM_API = 'https://graph.instagram.com/'

# fb

# tweetie


check_settings('SOCIALS', sys.modules[__name__], settings)
