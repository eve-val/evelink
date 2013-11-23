from evelink import server
from evelink.appengine.api import auto_async, auto_gae_api

@auto_async
class Server(server.Server):
    __doc__ = server.Server.__doc__

    @auto_gae_api
    def __init__(self, api=None):
        self.api = api
