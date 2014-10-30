import json
import re
import logging
from time import sleep

from evelink import api

from evelink.thirdparty.six.moves import urllib

_log = logging.getLogger('evelink.thirdparty.eve_who')


class FetchError(Exception):
    """Class for exceptions if fetch failed."""
    pass


class EVEWho(object):
    def __init__(self, url_fetch_func=None, cache=None, wait=True,
                 api_base='http://evewho.com/api.php'):
        super(EVEWho, self).__init__()

        self.api_base = api_base
        self.wait = wait

        if url_fetch_func is not None:
            self.url_fetch = url_fetch_func
        else:
            self.url_fetch = self._default_fetch_func

        cache = cache or api.APICache()
        if not isinstance(cache, api.APICache):
            raise ValueError("The provided cache must subclass from APICache.")
        self.cache = cache
        self.cachetime = 3600

    def _default_fetch_func(self, url):
        """Fetches a given URL using GET and returns the response."""
        return urllib.request.urlopen(url).read()

    def _cache_key(self, path, params):
        sorted_params = sorted(params.items())
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
                _log.error("Raising cached error: %r" % cached_result)
                raise cached_result
                # Normal cached results get returned
            _log.debug("Cache hit, returning cached payload")
            return cached_result

        query = urllib.parse.urlencode(params, True)
        url = '%s?%s' % (path, query)
        response = None

        regexp = re.compile("^hammering a website isn't very nice ya know.... please wait (\d+) seconds")
        hammering = True
        while hammering:
            response = self.url_fetch(url)
            hammering = regexp.findall(response)
            if hammering:
                if self.wait:
                    _log.debug("Fetch page waiting: %s (%s)" % (url, response))
                    sleep(int(hammering[0]))
                else:
                    _log.error("Fetch page error: %s (%s)" % (url, response))
                    raise FetchError(response)

        result = json.loads(response)
        self.cache.put(key, result, self.cachetime)
        return result

    def _member_list(self, ext_id, api_type):
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

            info = data['info']
            if info:
                member_count = int(info['member_count']) - 1    # workaround for numbers divisible by 200
            else:
                return members

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
        return self._member_list(corp_id, api_type='corplist')

    def alliance_member_list(self, alli_id):
        """Fetch member list for a alliance.

        (Convenience wrapper for member_list.)
        """
        return self._member_list(alli_id, api_type='allilist')
