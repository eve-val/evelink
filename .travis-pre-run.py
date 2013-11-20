#!/usr/bin/env python
#
#   Download and extract the last Google App Engine SDK.
#

import argparse
import logging
import os
import re
import sys
import urllib
from zipfile import ZipFile

import feedparser

GAE_FEED_URL = 'https://code.google.com/feeds/p/googleappengine/downloads/basic'
SDK_PATTERN = r'http://googleappengine.googlecode.com/files/google_appengine_(\d\.)+zip'
DEFAULT_URL = 'http://googleappengine.googlecode.com/files/google_appengine_1.8.8.zip'

_log = logging.getLogger('travis.prerun')
logging.basicConfig(level=logging.INFO)


def get_args_parser():
    """Build the command line argument parser

    """
    parser = argparse.ArgumentParser(
        description='Download and extract the last Google App Engine SDK to.'
    )
    parser.add_argument(
        'gae_lib_dst',
        nargs='?',
        default='/usr/local',
        help='directory to extract Google App Engine SDK '
            '(default to "/usr/local").'
    )
    return parser


def get_direct_link(entry):
    for link in entry.links:
        if link['rel'] == 'direct':
            return link['href']


def get_sdk_url(feed, pattern):
    _log.info("Fetching atom feed of the GAE sdk releases...")
    gae_feed = feedparser.parse(feed)
    for entry in gae_feed.entries:
        url = get_direct_link(entry)
        if re.match(pattern, url):
            return url


def download_sdk(url):
    _log.info("downloading SDK from %s ...", url)
    return urllib.urlretrieve(url)[0]


def unzip(file, dst):
    _log.info("Extracting SDK to %s ...", dst)
    with ZipFile(file) as z:
        for name in z.namelist():
            if '/' in name and name[0] == '/':
                raise ValueError("a SDK archive member has an absolute path")
            if '..' in name:
                raise ValueError("Found two dots in a member of the SDK archive")
        z.extractall(dst)


def main(gae_lib_dst):
    if sys.version_info[0:2] != (2, 7,):
        print "Google App Engine is not required."
        return
    
    try:
        url = get_sdk_url(GAE_FEED_URL, SDK_PATTERN)
        _log.info("Found GAE SDK url: %s", url)
    except Exception:
        url = DEFAULT_URL
        _log.info(
            "Failed finding GAE SDK url at %s; Will use default url (%s)",
            GAE_FEED_URL,
            url
        )

    try:
        if not os.path.exists(gae_lib_dst):
            _log.info("Creating %s directory", gae_lib_dst)
            os.makedirs(gae_lib_dst)

        sdk_path = download_sdk(url)
        unzip(sdk_path, gae_lib_dst)
        _log.info("GAE SDK available at %s/google_engine", gae_lib_dst)
    except Exception as e:
        _log.error("failed downloading the sdk: %s", str(e))


if __name__ == '__main__':
    parser = get_args_parser()
    args = parser.parse_args()
    main(args.gae_lib_dst)
