from google.appengine.api import memcache
from google.appengine.api import urlfetch
from evelink import api
import io


class AppengineAPI(api.API):
    """Subclass of api.API that is compatible with Google Appengine."""
    def __init__(self, base_url="api.eveonline.com", cache=None, api_key=None):
        cache = cache or AppengineCache()
        super(AppengineAPI, self).__init__(base_url=base_url,
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
            raise ValueError, "Bad result from server: {}".format(result.status_code)
        return io.BytesIO(result.content)


class AppengineCache(api.APICache):
    """Memcache backed APICache implementation."""
    def get(self, key):
        memcache.get(key)

    def put(self, key, value, duration):
        memcache.set(key, value, duration)
    
