import calendar
import functools
import logging
import re
import time
from urllib import urlencode
import urllib2
from xml.etree import ElementTree

_log = logging.getLogger('evelink.api')

def _clean(v):
    """Convert parameters into an acceptable format for the API."""
    if isinstance(v, (list, set, tuple)):
        return ",".join(str(i) for i in v)
    else:
        return str(v)


def parse_ts(v):
    """Parse a timestamp from EVE API XML into a unix-ish timestamp."""
    if v == '':
        return None
    ts = calendar.timegm(time.strptime(v, "%Y-%m-%d %H:%M:%S"))
    # Deal with EVE's nonexistent 0001-01-01 00:00:00 timestamp
    return ts if ts > 0 else None


def get_named_value(elem, field):
    """Returns the string value of the named child element."""
    try:
        return elem.find(field).text
    except AttributeError:
        return None


def get_ts_value(elem, field):
    """Returns the timestamp value of the named child element."""
    val = get_named_value(elem, field)
    if val:
        return parse_ts(val)
    return None


def get_int_value(elem, field):
    """Returns the integer value of the named child element."""
    val = get_named_value(elem, field)
    if val:
        return int(val)
    return val


def get_float_value(elem, field):
    """Returns the float value of the named child element."""
    val = get_named_value(elem, field)
    if val:
        return float(val)
    return val


def get_bool_value(elem, field):
    """Returns the boolean value of the named child element."""
    val = get_named_value(elem, field)
    if val == 'True':
        return True
    elif val == 'False':
        return False
    return None


def elem_getters(elem):
    """Returns a tuple of (_str, _int, _float, _bool, _ts) functions.

    These are getters closed around the provided element.
    """
    _str = lambda key: get_named_value(elem, key)
    _int = lambda key: get_int_value(elem, key)
    _float = lambda key: get_float_value(elem, key)
    _bool = lambda key: get_bool_value(elem, key)
    _ts = lambda key: get_ts_value(elem, key)

    return _str, _int, _float, _bool, _ts


def parse_keyval_data(data_string):
    """Parse 'key: value' lines from a LF-delimited string."""
    keyval_pairs = data_string.strip().split('\n')
    results = {}
    for pair in keyval_pairs:
        key, _, val = pair.strip().partition(': ')

        if 'Date' in key:
            val = parse_ms_date(val)
        elif val == 'null':
            val = None
        elif re.match(r"^-?\d+$", val):
            val = int(val)
        elif re.match(r"-?\d+\.\d+", val):
            val = float(val)

        results[key] = val
    return results

def parse_ms_date(date_string):
    """Convert MS date format into epoch"""

    return int(date_string)/10000000 - 11644473600;

class APIError(Exception):
    """Exception raised when the EVE API returns an error."""

    def __init__(self, code=None, message=None):
        self.code = code
        self.message = message

    def __repr__(self):
        return "APIError(%r, %r)" % (self.code, self.message)

    def __str__(self):
        return "%s (code=%d)" % (self.message, int(self.code))

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

    def __init__(self, base_url="api.eveonline.com", cache=None, api_key=None):
        self.base_url = base_url

        cache = cache or APICache()
        if not isinstance(cache, APICache):
            raise ValueError("The provided cache must subclass from APICache.")
        self.cache = cache

        if api_key and len(api_key) != 2:
            raise ValueError("The provided API key must be a tuple of (keyID, vCode).")
        self.api_key = api_key

    def _cache_key(self, path, params):
        sorted_params = sorted(params.iteritems())
        # Paradoxically, Shelve doesn't like integer keys.
        return str(hash((path, tuple(sorted_params))))

    def get(self, path, params=None):
        """Request a specific path from the EVE API.

        The supplied path should be a slash-separated path
        frament, e.g. "corp/AssetList". (Basically, the portion
        of the API url in between the root / and the .xml bit.)
        """

        params = params or {}
        params = dict((k, _clean(v)) for k,v in params.iteritems())

        _log.debug("Calling %s with params=%r", path, params)
        if self.api_key:
            _log.debug("keyID and vCode added")
            params['keyID'] = self.api_key[0]
            params['vCode'] = self.api_key[1]

        key = self._cache_key(path, params)
        cached_result = self.cache.get(key)
        if cached_result is not None:
            # Cached APIErrors should be re-raised
            if isinstance(cached_result, APIError):
                _log.error("Raising cached error: %r" % cached_result)
                raise cached_result
            # Normal cached results get returned
            _log.debug("Cache hit, returning cached payload")
            return cached_result

        params = urlencode(params)

        full_path = "https://%s/%s.xml.aspx" % (self.base_url, path)

        response = self.send_request(full_path, params)

        tree = ElementTree.parse(response)

        current_time = get_ts_value(tree, 'currentTime')
        expires_time = get_ts_value(tree, 'cachedUntil')

        error = tree.find('error')
        if error is not None:
            code = error.attrib['code']
            message = error.text.strip()
            exc = APIError(code, message)

            self.cache.put(key, exc, expires_time - current_time)
            _log.error("Raising API error: %r" % exc)
            raise exc

        result = tree.find('result')

        self.cache.put(key, result, expires_time - current_time)
        return result

    def send_request(self, full_path, params):
        try:
            if params:
                # POST request
                _log.debug("POSTing request")
                return urllib2.urlopen(full_path, params)
            else:
                # GET request
                _log.debug("GETting request")
                return urllib2.urlopen(full_path)
        except urllib2.URLError as e:
            # TODO: Handle this better?
            raise e

def auto_api(func):
    """A decorator to automatically provide an API instance.

    Functions decorated with this will have the api= kwarg
    automatically supplied with a default-initialized API()
    object if no other API object is supplied.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'api' not in kwargs:
            kwargs['api'] = API()
        return func(*args, **kwargs)
    return wrapper


# vim: set ts=4 sts=4 sw=4 et:
