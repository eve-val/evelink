#!/usr/bin/env python
#
#   Download and extract the last Google App Engine SDK.
#

import argparse
import json
import logging
import os
import re
import sys
from evelink.thirdparty.six.moves import urllib
from zipfile import ZipFile


GAE_SDK_DOWNLOAD_LIST = 'https://www.googleapis.com/storage/v1/b/appengine-sdks/o?prefix=featured'
SDK_FILE_PATTERN = re.compile(r'google_appengine_([0-9.]+)\.zip')
DEFAULT_URL = 'https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.40.zip'

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


def get_sdk_url(api_url, pattern):
    try:
        _log.info("Fetching GAE sdk releases...")
        f = urllib.request.urlopen(api_url)
        data = json.loads(f.read())
    finally:
        f.close()

    medialinks = [item['mediaLink'] for item in data['items']]
    python_sdks = [i for i in medialinks if pattern.search(i)]
    if python_sdks:
      # lazy version sort
      python_sdks.sort(key=lambda x: x.split('.'), reverse=True)
      return python_sdks[0]
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
        url = get_sdk_url(GAE_SDK_DOWNLOAD_LIST, SDK_FILE_PATTERN)
        _log.info("Found GAE SDK url: %s", url)
    except Exception as e:
        _log.error(e)
        url = DEFAULT_URL
        _log.info(
            "Failed finding GAE SDK url at %s; Will use default url (%s)",
            GAE_SDK_DOWNLOAD_LIST,
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
