from google.appengine.ext import ndb

from evelink import eve, api
from evelink.appengine.api import auto_async, auto_gae_api

@auto_async
class EVE(eve.EVE):
    __doc__ = eve.EVE.__doc__

    @auto_gae_api
    def __init__(self, api=None):
        self.api = api

    @ndb.tasklet
    def character_name_from_id_async(self, char_id):
        """Asynchronous version of character_name_from_id."""
        resp = yield self.character_names_from_ids_async([char_id])
        raise ndb.Return(
            api.APIResult(
                resp.result.get(char_id), resp.timestamp, resp.expires
            )
        )

    @ndb.tasklet
    def character_id_from_name_async(self, name):
        """Asynchronous version of character_id_from_name."""
        resp = yield self.character_ids_from_names_async([name])
        raise ndb.Return(
            api.APIResult(resp.result.get(name), resp.timestamp, resp.expires)
        )
