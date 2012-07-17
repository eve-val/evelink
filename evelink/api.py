import calendar
import time
from urllib import urlencode
import urllib2
from xml.etree import ElementTree


def _clean(v):
    """Convert parameters into an acceptable format for the API."""
    if isinstance(v, (list, set, tuple)):
        return ",".join(str(i) for i in v)
    else:
        return str(v)


def _parse_ts(v):
    """Parse a timestamp from EVE API XML into a unix-ish timestamp."""
    return calendar.timegm(time.strptime(v, "%Y-%m-%d %H:%M:%S"))


class APICache(object):
    """Minimal interface for caching API requests.
    
    This very basic implementation simply stores values in
    memory, with no other persistence. You can subclass it
    to define a more complex/featureful/persistent cache.
    """

    def __init__(self):
        self.cache = {}

    def get(self, key):
        """Return the value referred to by 'key' if it is cached.

        key:
            a result from the Python hash() function.
        """
        result = self.cache.get(key)
        if not result:
            return None
        value, expiration = result
        if expiration < time.time():
            del self.cache[key]
            return None
        return value

    def put(self, key, value, duration):
        """Cache the provided value, referenced by 'key', for the given duration.

        key:
            a result from the Python hash() function.
        value:
            an xml.etree.ElementTree.Element object
        duration:
            a number of seconds before this cache entry should expire.
        """
        expiration = time.time() + duration
        self.cache[key] = (value, expiration)


class API(object):
    """A wrapper around the EVE API."""

    def __init__(self, base_url="api.eveonline.com", cache=None):
        self.base_url = base_url

        cache = cache or APICache()
        if not isinstance(cache, APICache):
            raise ValueError("The provided cache must subclass from APICacheBase.")
        self.cache = cache

    def _cache_key(self, path, params):
        sorted_params = sorted(params.iteritems())
        return hash((path, tuple(sorted_params)))

    def get(self, path, params=None):
        """Request a specific path from the EVE API.

        The supplied path should be a slash-separated path
        frament, e.g. "corp/AssetList". (Basically, the portion
        of the API url in between the root / and the .xml bit.)
        """

        params = params or {}
        params = dict((k, _clean(v)) for k,v in params.iteritems())

        key = self._cache_key(path, params)
        cached_result = self.cache.get(key)
        if cached_result is not None:
            return cached_result

        params = urlencode(params)

        full_path = "https://%s/%s.xml.aspx" % (self.base_url, path)

        try:
            if params:
                # POST request
                response = urllib2.urlopen(full_path, params)
            else:
                # GET request
                response = urllib2.urlopen(full_path)
        except urllib2.URLError as e:
            # TODO: Handle this better?
            raise e

        tree = ElementTree.parse(response)
        result = tree.find('result')

        current_time = _parse_ts(tree.find('currentTime').text)
        expires_time = _parse_ts(tree.find('cachedUntil').text)

        self.cache.put(key, result, expires_time - current_time)
        return result
