#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Luke Woloszyn'
SITEURL = u'http://lukewoloszyn.com'
SITENAME = u'Luke Woloszyn'
SITESUBTITLE = u'data scientist, outdoor enthusiast, music lover, sports fan'

ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}.html'

RELATIVE_URLS = True

TYPOGRIFY = True

THEME = '../crowsfoot'

# PATH = 'content'
ARTICLE_PATHS = ['blog']

# MENUITEMS = [('blog', '/'), ('cv', '/misc/cv.pdf')]
MENUITEMS = [('Blog', '/'), ]
PROFILE_IMAGE_URL = '/images/personal.jpg'

STATIC_PATHS = ['images', 'extra/robots.txt', 'extra/favicon.ico', 'misc']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
}

PLUGIN_PATHS = ['../pelican-plugins']
PLUGINS = ['render_math']

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = u'en'

DEFAULT_PAGINATION = None

# addresses
EMAIL_ADDRESS = 'luke.woloszyn@gmail.com'
GITHUB_ADDRESS = 'https://github.com/lwoloszy'
LINKEDIN_ADDRESS = 'https://www.linkedin.com/in/lukewoloszyn'
TWITTER_ADDRESS = 'https://www.twitter.com/lukewoloszyn'

# feed
FEED_RSS = 'feeds/rss.xml'
FEED_MAX_ITEMS = 10

SHOW_ARTICLE_AUTHOR = False

LICENSE_NAME = "CC BY-SA"
LICENSE_URL = "https://creativecommons.org/licenses/by-sa/3.0/"

LOAD_CONTENT_CACHE = False
