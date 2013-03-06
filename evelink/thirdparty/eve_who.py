import json
import urllib
import re
from evelink import api
from time import sleep

try:
    import urllib2
except ImportError:
    urllib2 = None


class EVEWho(object):
    def __init__(self, url_fetch_func=None, cache=None,
                 api_base='http://evewho.com/api.php'):
        super(EVEWho, self).__init__()

        self.api_base = api_base

        if url_fetch_func is not None:
            self.url_fetch = url_fetch_func
        elif urllib2 is not None:
            self.url_fetch = self._default_fetch_func
        else:
            raise ValueError("urllib2 not available - specify url_fetch_func")

        cache = cache or api.APICache()
        if not isinstance(cache, api.APICache):
            raise ValueError("The provided cache must subclass from APICache.")
        self.cache = cache
        self.cachetime = 3600

    def _default_fetch_func(self, url):
        """Fetches a given URL using GET and returns the response."""
        return urllib2.urlopen(url).read()

    def _cache_key(self, path, params):
        sorted_params = sorted(params.iteritems())
        # Paradoxically, Shelve doesn't like integer keys.
        return str(hash((path, tuple(sorted_params))))

    def _get(self, ext_id, api_type, page=0):
        """Request page from EveWho api."""
        path = self.api_base
        params = {'id': ext_id,
                  'type': api_type,
                  'page': page}

        key = self._cache_key(path, params)
        cached_result = self.cache.get(key)
        if cached_result is not None:
            # Cached APIErrors should be re-raised
            if isinstance(cached_result, api.APIError):
                api.log.error("Raising cached error: %r" % cached_result)
                raise cached_result
                # Normal cached results get returned
            api.log.debug("Cache hit, returning cached payload")
            return cached_result

        query = urllib.urlencode(params, True)
        url = '%s?%s' % (path, query)
        response = None

        regexp = re.compile("^hammering a website isn't very nice ya know.... please wait (\d+) seconds")
        wait = True
        while wait:
            response = self.url_fetch(url)
            wait = regexp.findall(response)
            if wait:
                sleep(float(wait[0]))

        result = json.loads(response)
        self.cache.put(key, result, self.cachetime)
        return result

    def member_list(self, ext_id, api_type):
        """Fetches member list for corporation or alliance.

        Valid api_types: 'corplist', 'allilist'.
        """
        if api_type not in ['corplist', 'allilist']:
            raise ValueError("not valid api type - valid api types: 'corplist' and 'allilist'.")

        member_count = 0
        page = 0
        members = []
        while page <= (member_count // 200):
            data = self._get(ext_id, api_type, page)
            member_count = int(data['info']['member_count'])

            for member in data['characters']:
                members.append({'name': str(member['name']),
                                'char_id': int(member['character_id']),
                                'corp_id': int(member['corporation_id']),
                                'alli_id': int(member['alliance_id'])})
            page += 1

        return members

    def corp_member_list(self, corp_id):
        """Fetch member list for a corporation.

        (Convenience wrapper for member_list.)
        """
        return self.member_list(corp_id, api_type='corplist')

    def alli_member_list(self, alli_id):
        """Fetch member list for a alliance.

        (Convenience wrapper for member_list.)
        """
        return self.member_list(alli_id, api_type='allilist')

# vim: set et ts=4 sts=4 sw=4:
