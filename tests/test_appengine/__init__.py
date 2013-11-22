import sys
import unittest2 as unittest

import mock

try:
    from google.appengine.ext import ndb
except ImportError:
    NO_GAE = True
else:
    NO_GAE = False


@unittest.skipIf(sys.version_info[0:2] != (2, 7,), 'GAE requires python 2.7')
@unittest.skipIf(NO_GAE, 'No GAE SDK found')
class GAETestCase(unittest.TestCase):
    """
    Those test cases require python 2.7 and the Google App Engine SDK 
    to be installed.

    """