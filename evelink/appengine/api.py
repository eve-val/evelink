import functools
import inspect
import time
from urllib import urlencode
from xml.etree import ElementTree

from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

from evelink import api


class UrlFetchError(Exception): pass


class AppEngineAPI(api.API):
    """Subclass of api.API that is compatible with Google Appengine."""

    def __init__(self, base_url="api.eveonline.com", cache=None, api_key=None):
        cache = cache or AppEngineCache()
        super(AppEngineAPI, self).__init__(base_url=base_url,
                cache=cache, api_key=api_key)

    @ndb.tasklet
    def get_async(self, path, params=None):
        """Asynchronous request a specific path from the EVE API.

        TODO: refactor evelink.api.API.get
        """

        params = params or {}
        params = dict((k, api._clean(v)) for k,v in params.items())

        if self.api_key:
            params['keyID'] = self.api_key[0]
            params['vCode'] = self.api_key[1]

        key = self._cache_key(path, params)
        response = yield self.cache.get_async(key)
        cached = response is not None

        if not cached:
            # no cached response body found, call the API for one.
            params = urlencode(params)
            full_path = "https://%s/%s.xml.aspx" % (self.base_url, path)
            response, robj = yield self.send_request_async(full_path, params)

        try:
            tree = ElementTree.fromstring(response)
        except ElementTree.ParseError as e:
            self.maybe_raise_http_error(robj)
            raise e

        current_time = api.get_ts_value(tree, 'currentTime')
        expires_time = api.get_ts_value(tree, 'cachedUntil')
        self._set_last_timestamps(current_time, expires_time)

        if not cached:
            yield self.cache.put_async(key, response, expires_time - current_time)

        error = tree.find('error')
        if error is not None:
            code = error.attrib['code']
            message = error.text.strip()
            exc = api.APIError(code, message, current_time, expires_time)
            raise exc

        result = tree.find('result')
        raise ndb.Return(api.APIResult(result, current_time, expires_time))

    def maybe_raise_http_error(self, robj):
        if robj.status_code != 200:
            raise UrlFetchError(
                "HTTP error {0}".format(robj.status_code),
                robj.status_code)

    def send_request(self, url, params):
        """Send a request via the urlfetch API.

        url:
            The url to fetch
        params:
            URL encoded parameters to send. If set, will use a form POST,
            otherwise a GET.
        """
        params = urlencode(params)
        return self.send_request_async(url, params).get_result()

    @ndb.tasklet
    def send_request_async(self, url, params):
        ctx = ndb.get_context()
        headers = {'User-agent': self.user_agent}
        if params:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        result = yield ctx.urlfetch(
            url=url,
            payload=params,
            method=urlfetch.POST if params else urlfetch.GET,
            headers=headers,
            deadline=api.http_request_timeout,
        )
        raise ndb.Return((result.content, result))


class AppEngineCache(api.APICache):
    """Memcache backed APICache implementation."""

    def get(self, key):
        return memcache.get(key)

    @ndb.tasklet
    def get_async(self, key):
        """Dummy async method.

        Memcache doesn't have an async get method.
        """
        raise ndb.Return(self.get(key))


    def put(self, key, value, duration):
        if duration < 0:
            duration = time.time() + duration
        memcache.set(key, value, time=duration)

    @ndb.tasklet
    def put_async(self, key,  value, duration):
        """Dummy async method (see get_async)."""
        self.put(key, value, duration)


class EveLinkCache(ndb.Model):
    value = ndb.PickleProperty()
    expiration = ndb.IntegerProperty()


class AppEngineDatastoreCache(api.APICache):
    """An implementation of APICache using the AppEngine datastore."""

    def __init__(self):
        super(AppEngineDatastoreCache, self).__init__()

    def get(self, cache_key):
        return self.get_async(cache_key).get_result()

    @ndb.tasklet
    def get_async(self, cache_key):
        db_key = ndb.Key(EveLinkCache, cache_key)
        result = yield db_key.get_async()

        if not result:
            raise ndb.Return(None)

        if result.expiration < time.time():
            yield db_key.delete_async()
            raise ndb.Return(None)

        raise ndb.Return(result.value)

    def put(self, cache_key, value, duration):
        self.put_async(cache_key, value, duration).get_result()

    @ndb.tasklet
    def put_async(self, cache_key, value, duration):
        expiration = int(time.time() + duration)
        cache = EveLinkCache(id=cache_key, value=value, expiration=expiration)
        yield cache.put_async()


def auto_gae_api(func):
    """A decorator to automatically provide an AppEngineAPI instance."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        defaultargs, defaultkwargs = api.get_args_and_defaults(func)
        mapped_args = api.map_func_args(args, kwargs, defaultargs, defaultkwargs)
        if mapped_args.get('api') is None:
            kwargs['api'] = AppEngineAPI()
        return func(*args, **kwargs)
    return wrapper


def _make_async(method):
    def _async(self, *args, **kw):
        # method specs
        path = method._request_specs['path']
        args_names = method._request_specs['args']
        defaults = method._request_specs['defaults']
        prop_to_param = method._request_specs['prop_to_param']
        map_params = method._request_specs['map_params']

        # build parameter map
        args_map = api.map_func_args(args, kw, args_names, defaults)
        for attr_name in prop_to_param:
            args_map[attr_name] = getattr(self, attr_name, None)

        # fix params name and remove params with None values
        params = api.translate_args(args_map, map_params)
        params =  dict((k, v,) for k, v in params.items() if v is not None)

        kw['api_result'] = yield self.api.get_async(path, params=params)
        raise ndb.Return(method(self, *args, **kw))
    return ndb.tasklet(_async)


def auto_async(cls):
    """Class decoration which add a async version of any method with a
    a '_request_specs' attribute (metadata added by api.auto_add).
    """
    for method_name, method in inspect.getmembers(cls, inspect.ismethod):
        if not hasattr(method, '_request_specs'):
            continue

        async_method = _make_async(method)
        async_method.__doc__ = """Asynchronous version of %s.""" % method_name
        async_method.__name__ = '%s_async' % method_name
        setattr(cls, async_method.__name__, async_method)

    return cls
