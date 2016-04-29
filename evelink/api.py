import calendar
import collections
import functools
import zlib
import inspect
import logging
import re
import time
import hashlib
from xml.etree import ElementTree

from evelink.thirdparty import six
from evelink.thirdparty.six.moves import urllib

_log = logging.getLogger('evelink.api')

# Python 2.6's ElementTree raises xml.parsers.expat.ExpatError instead
# of ElementTree.ParseError
_xml_error = getattr(ElementTree, 'ParseError', None)
if _xml_error is None:
    import xml.parsers.expat
    _xml_error = xml.parsers.expat.ExpatError

# Allows zlib.decompress to decompress gzip-compressed strings as well.
# From zlib.h header file, not documented in Python.
ZLIB_DECODE_AUTO = 32 + zlib.MAX_WBITS

# Set by evelink/__init__.py to the evelink version. Use the user_agent
# parameter when constructing an API object if you want to add additional
# information to the user agent string. (Technically, you *can* override
# this, but it's not the intended method.)
_user_agent = None

# Can be set to an APICache instance that is used as a shared default
# cache instance for all API instances. Note: instance, not class.
default_cache = None

# The timeout to use for API HTTP requests, in seconds (default 1 minute).
http_request_timeout = 60

try:
    import requests
    _has_requests = True
except ImportError:
    _log.info('`requests` not available, falling back to urllib2')
    _has_requests = None

def _clean(v):
    """Convert parameters into an acceptable format for the API."""
    if isinstance(v, (list, set, tuple)):
        return ",".join(str(i) for i in v)
    else:
        return str(v)

def decompress(s):
    """Decode a gzip compressed string."""
    return zlib.decompress(s, ZLIB_DECODE_AUTO)


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

    def __init__(self, code=None, message=None, timestamp=None, expires=None):
        self.code = code
        self.message = message
        self.timestamp = timestamp
        self.expires = expires

    def __repr__(self):
        return "APIError(%r, %r, timestamp=%r, expires=%r)" % (
            self.code, self.message, self.timestamp, self.expires)

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
            a string hash key
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
            a string hash key
        value:
            an xml.etree.ElementTree.Element object
        duration:
            a number of seconds before this cache entry should expire.
        """
        expiration = time.time() + duration
        self.cache[key] = (value, expiration)


APIResult = collections.namedtuple("APIResult", [
        "result",
        "timestamp",
        "expires",
    ])


class API(object):
    """A wrapper around the EVE API."""

    def __init__(self,
                 base_url="api.eveonline.com", cache=None,
                 api_key=None, user_agent=None, sso_token=None):
        self.base_url = base_url
        self.user_agent = _user_agent

        if user_agent is not None:
            self.user_agent += ' %s' % user_agent

        cache = cache or default_cache or APICache()
        if not isinstance(cache, APICache):
            raise ValueError("The provided cache must subclass from APICache.")
        self.cache = cache
        self.CACHE_VERSION = '1'

        if api_key and len(api_key) != 2:
            raise ValueError("The provided API key must be a tuple of (keyID, vCode).")
        self.api_key = api_key
        if sso_token and len(sso_token) != 2:
            # TODO: maybe allow omitting type somehow? For now this is easier.
            raise ValueError("The provided SSO token must be a tuple of (token, type).")
        self.sso_token = sso_token
        self._set_last_timestamps()

    def _set_last_timestamps(self, current_time=0, cached_until=0):
        self.last_timestamps = {
            'current_time': current_time,
            'cached_until': cached_until,
        }

    def _cache_key(self, path, params):
        sorted_params = sorted(params.items())
        # Paradoxically, Shelve doesn't like integer keys.
        return '%s-%s' % (self.CACHE_VERSION, hashlib.sha1(str([path,sorted_params]).encode("utf-8")).hexdigest())

    def get(self, path, params=None):
        """Request a specific path from the EVE API.

        The supplied path should be a slash-separated path
        frament, e.g. "corp/AssetList". (Basically, the portion
        of the API url in between the root / and the .xml bit.)
        """

        params = params or {}
        params = dict((k, _clean(v)) for k,v in params.items())

        _log.debug("Calling %s with params=%r", path, params)
        if self.sso_token:
            _log.debug("SSO token added")
            params['accessToken'] = self.sso_token[0]
            params['accessType'] = self.sso_token[1]
        elif self.api_key:
            _log.debug("keyID and vCode added")
            params['keyID'] = self.api_key[0]
            params['vCode'] = self.api_key[1]

        key = self._cache_key(path, params)
        response = self.cache.get(key)
        cached = response is not None

        if not cached:
            # no cached response body found, call the API for one.
            full_path = "https://%s/%s.xml.aspx" % (self.base_url, path)
            response, robj = self.send_request(full_path, params)
        else:
            _log.debug("Cache hit, returning cached payload")

        try:
            tree = ElementTree.fromstring(response)
        except _xml_error as e:
            # If this is due to an HTTP error, raise the HTTP error
            self.maybe_raise_http_error(robj)
            # otherwise, raise the parse error
            raise e

        current_time = get_ts_value(tree, 'currentTime')
        expires_time = get_ts_value(tree, 'cachedUntil')
        self._set_last_timestamps(current_time, expires_time)

        if not cached:
            # Have to split this up from above as timestamps have to be
            # extracted.
            self.cache.put(key, response, expires_time - current_time)

        error = tree.find('error')
        if error is not None:
            code = error.attrib['code']
            message = error.text.strip()
            exc = APIError(code, message, current_time, expires_time)
            _log.debug("Raising API error: %r" % exc)
            raise exc

        result = tree.find('result')
        return APIResult(result, current_time, expires_time)

    def maybe_raise_http_error(self, response):
        """Called if a XML parse error is raised for the response.

        Raises an error if the response itself was an error - we try
        to parse it as XML first to see if it's an API error, but if
        it's not, this method gets called.
        """
        if _has_requests:
            # Requests has a built-in method for this functionality
            response.raise_for_status()
        else:
            # urllib2 uses exceptions by default for this, which we've
            # potentially previously caught and stored as the response
            if isinstance(response, Exception):
                raise response

    def send_request(self, full_path, params):
        if _has_requests:
            return self.requests_request(full_path, params)
        else:
            return self.urllib2_request(full_path, params)

    def urllib2_request(self, full_path, params):
        r = None
        try:
            if params:
                # POST request
                _log.debug("POSTing request")
                params = urllib.parse.urlencode(params)
                req = urllib.request.Request(full_path, data=params.encode())
            else:
                # GET request
                req = urllib.request.Request(full_path)
                _log.debug("GETting request")

            req.add_header('Accept-Encoding', 'gzip')
            req.add_header('User-agent', self.user_agent)
            r = urllib.request.urlopen(req, timeout=http_request_timeout)
        except urllib.error.HTTPError as e:
            # urllib2 handles non-2xx responses by raising an exception that
            # can also behave as a file-like object. The EVE API will return
            # non-2xx HTTP codes on API errors (since Odyssey, apparently)
            r = e
        except urllib.error.URLError as e:
            # TODO: Handle this better?
            raise e

        try:
            if r.info().get('Content-Encoding') == 'gzip':
                return decompress(r.read()), r
            else:
                return r.read(), r
        finally:
            r.close()

    def requests_request(self, full_path, params):
        session = getattr(self, 'session', None)
        if not session:
            session = requests.Session()
            session.headers.update({'User-Agent': self.user_agent})
            self.session = session

        try:
            if params:
                # POST request
                _log.debug("POSTing request")
                r = session.post(full_path, data=params, timeout=http_request_timeout)
            else:
                # GET request
                _log.debug("GETting request")
                r = session.get(full_path, timeout=http_request_timeout)
            _log.debug("Response status code: %s" % r.status_code)
            return r.content, r
        except requests.exceptions.RequestException as e:
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
        defaultargs, defaultkwargs = get_args_and_defaults(func)
        mapped_args = map_func_args(args, kwargs, defaultargs, defaultkwargs)
        if mapped_args.get('api') is None:
            kwargs['api'] = API()
        return func(*args, **kwargs)
    return wrapper


def translate_args(args, mapping=None):
    """Translate python name variable into API parameter name."""
    mapping = mapping if mapping else {}
    return dict((mapping[k], v,) for k, v in args.items())

# TODO: needs better name
def get_args_and_defaults(func):
    """Return the list of argument names and a dict of default values"""
    specs = inspect.getargspec(func)
    return (
        specs.args,
        dict(zip(specs.args[-len(specs.defaults):], specs.defaults)),
    )


def map_func_args(args, kw, args_names, defaults):
    """Associate positional (*args) and key (**kw) arguments values
    with their argument names.

    'args_names' should be the list of argument names and 'default'
    should be a dict associating the keyword arguments to their
    defaults.

    Similar to inspect.getcallargs() but compatible with python 2.6.

    """
    if (len(args)+len(kw)) > len(args_names):
        raise TypeError('Too many arguments.')

    map_ = dict(zip(args_names, args))
    for k, v in kw.items():
        if k in map_:
            raise TypeError(
                "got multiple values for keyword argument '%s'" % k
            )
        map_[k] = v

    for k, v in defaults.items():
        map_.setdefault(k, v)

    required_args = args_names[0:-len(defaults)]
    for k in required_args:
        if k not in map_:
            raise TypeError("Too few arguments")
    return map_


class auto_call(object):
    """A decorator to automatically provide an api response to a method.

    The object the method will be bound to should have an api attribute
    and the method should have a keyword argument named 'api_result'.

    The decorated method will have a '_request_specs' dict attribute
    holding:

    - 'path': path of the request needs to be queried.

    - 'args': method argument names.

    - 'defaults': method keyword arguments and theirs default value.

    - 'prop_to_param': properties of the instance the method is bound
    to to add as parameter of api request.

    - 'map_params': dictionary associating argument name to a
    paramater name. They will be added to 'evelink.api._args_map' to
    translate argument names to parameter names.

    """

    def __init__(self, path, prop_to_param=tuple(), map_params=None):
        self.method = None

        self.path = path
        self.args = None
        self.defaults = None
        self.prop_to_param = prop_to_param
        self.map_params = map_params if map_params else {}

    def __call__(self, method):
        if self.method is not None:
            raise TypeError("This decorator method cannot be shared.")
        self.method = method

        wrapper = self._wrapped_method()

        args, self.defaults = get_args_and_defaults(self.method)

        self.args = args[1:]
        self.args.remove('api_result')
        self.defaults.pop('api_result')  # TODO: better exception

        wrapper._request_specs = {
            'path': self.path,
            'args': self.args,
            'defaults': self.defaults,
            'prop_to_param': self.prop_to_param,
            'map_params': self.map_params
        }

        return wrapper

    def _wrapped_method(self):

        @functools.wraps(self.method)
        def wrapper(client, *args, **kw):
            if 'api_result' in kw:
                return self.method(client, *args, **kw)

            args_map = map_func_args(args, kw, self.args, self.defaults)
            for attr_name in self.prop_to_param:
                args_map[attr_name] = getattr(client, attr_name, None)

            params = translate_args(args_map, self.map_params)
            params =  dict((k, v,) for k, v in params.items() if v is not None)

            kw['api_result'] = client.api.get(self.path, params=params)
            return self.method(client, *args, **kw)

        return wrapper


# vim: set ts=4 sts=4 sw=4 et:
