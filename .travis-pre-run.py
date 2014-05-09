#!/usr/bin/env python
#
#   Download and extract the last Google App Engine SDK.
#

import argparse
import logging
import os
import re
import sys
from evelink.thirdparty.six.moves import urllib
from xml.etree import ElementTree as ET
from zipfile import ZipFile


GAE_FEED_URL = 'https://code.google.com/feeds/p/googleappengine/downloads/basic'
SDK_PATTERN = r'http://googleappengine.googlecode.com/files/google_appengine_(\d\.)+zip'
DEFAULT_URL = 'http://googleappengine.googlecode.com/files/google_appengine_1.8.9.zip'

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


def get_sdk_url(feed, pattern):
    try:
        _log.info("Fetching atom feed for GAE sdk releases...")
        f = urllib.request.urlopen(feed)
        tree = ET.fromstring(f.read())
    finally:
        f.close()

    ns = {'a': 'http://www.w3.org/2005/Atom'}
    for link in tree.findall("a:entry/a:link[@rel='direct']", namespaces=ns):
        url = link.get('href')
        if re.match(SDK_PATTERN, url):
            _log.info("Found last release: %s", url)
            return url
    raise ValueError("No download links found!")


def download_sdk(url):
    _log.info("downloading SDK from %s ...", url)
    return urllib.request.urlretrieve(url)[0]


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
        _log.info("Python 2.7 is required to run AppEngine.")
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
