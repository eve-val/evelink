from evelink import map as map_
from evelink.appengine.api import auto_async, auto_gae_api


@auto_async
class Map(map_.Map):
    __doc__ = map_.Map.__doc__

    @auto_gae_api
    def __init__(self, api=None):
        self.api = api
