import shelve

from evelink import api

class ShelveCache(api.APICache):
    """An implementation of APICache using shelve."""

    def __init__(self, path):
        super(ShelveCache, self).__init__()
        self.cache = shelve.open(path)
