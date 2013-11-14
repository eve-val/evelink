from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from evelink import api
import time


class AppEngineAPI(api.API):
    """Subclass of api.API that is compatible with Google Appengine."""
    def __init__(self, base_url="api.eveonline.com", cache=None, api_key=None):
        cache = cache or AppEngineCache()
        super(AppEngineAPI, self).__init__(base_url=base_url,
                cache=cache, api_key=api_key)

    def send_request(self, url, params):
        """Send a request via the urlfetch API.

        url:
            The url to fetch
        params:
            URL encoded parameters to send. If set, will use a form POST,
            otherwise a GET.
        """
        result = urlfetch.fetch(
                url=url,
                payload=params,
                method=urlfetch.POST if params else urlfetch.GET,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
                        if params else {}
                )
        if result.status_code != 200:
            raise ValueError("Bad result from server: {}".format(result.status_code))
        return result.content


class AppEngineCache(api.APICache):
    """Memcache backed APICache implementation."""
    def get(self, key):
        memcache.get(key)

    def put(self, key, value, duration):
        if duration < 0:
            duration = time.time() + duration
        memcache.set(key, value, time=duration)


class EveLinkCache(ndb.Model):
    value = ndb.PickleProperty()
    expiration = ndb.IntegerProperty()


class AppEngineDatastoreCache(api.APICache):
    """An implementation of APICache using the AppEngine datastore."""

    def __init__(self):
        super(AppEngineDatastoreCache, self).__init__()

    def get(self, cache_key):
        db_key = ndb.Key(EveLinkCache, cache_key)
        result = db_key.get()
        if not result:
            return None
        if result.expiration < time.time():
            db_key.delete()
            return None
        return result.value

    def put(self, cache_key, value, duration):
        expiration = int(time.time() + duration)
        cache = EveLinkCache.get_or_insert(cache_key)
        cache.value = value
        cache.expiration = expiration
        cache.put()
