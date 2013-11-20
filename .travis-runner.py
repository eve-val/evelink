#!/usr/bin/env python
#
# Test runner for Travis
# 

import sys
import unittest2

GAE_SDK_PATH = './vendors/google_appengine/'
TEST_PATH = './tests/'


def setup_gae(sdk_path):
    if sys.version_info < (2, 7,):
        return

    sys.path.insert(0, sdk_path)
    import dev_appserver
    dev_appserver.fix_sys_path()

def main(sdk_path, test_path):
    setup_gae(sdk_path)
    suite = unittest2.loader.TestLoader().discover(test_path)
    return unittest2.TextTestRunner(verbosity=2, buffer=True).run(suite)

if __name__ == '__main__':
    results = main(GAE_SDK_PATH, TEST_PATH)
    if not results.wasSuccessful():
    	sys.exit(1)
