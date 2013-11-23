from google.appengine.ext import ndb

from evelink import map as map_
from evelink.appengine.api import auto_gae_api


class Map(map_.Map):
    __doc__ = map_.Map.__doc__

    @auto_gae_api
    def __init__(self, api=None):
        self.api = api

    @ndb.tasklet
    def jumps_by_system_async(self):
        """Asynchronous version of jumps_by_system."""
        api_result = yield self.api.get_async('map/Jumps')
        raise ndb.Return(self.jumps_by_system(api_result=api_result))

    @ndb.tasklet
    def kills_by_system_async(self):
    	"""Asynchronous version of kills_by_system."""
        api_result = yield self.api.get_async('map/Kills')
        raise ndb.Return(self.kills_by_system(api_result=api_result))

    @ndb.tasklet
    def faction_warfare_systems_async(self):
        """Asynchronous version of action_warfare_systems."""
        api_result = yield self.api.get_async('map/FacWarSystems')
        raise ndb.Return(self.faction_warfare_systems(api_result=api_result))

    @ndb.tasklet
    def sov_by_system_async(self):
        """Asynchronous version of sov_by_system."""
        api_result = yield self.api.get_async('map/Sovereignty')
        raise ndb.Return(self.sov_by_system(api_result=api_result))
