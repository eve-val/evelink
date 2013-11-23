from google.appengine.ext import ndb

from evelink import api, eve
from evelink.appengine.api import auto_gae_api

class EVE(eve.EVE):
    __doc__ = eve.EVE.__doc__

    @auto_gae_api
    def __init__(self, api=None):
        self.api = api

    @ndb.tasklet
    def certificate_tree_async(self):
        """Asynchronous version of certificate_tree."""
        api_result = yield self.api.get_async('eve/CertificateTree')
        raise ndb.Return(self.certificate_tree(api_result=api_result))
        
    @ndb.tasklet
    def character_names_from_ids_async(self, id_list):
        """Asynchronous version of character_names_from_ids."""
        api_result = yield self.api.get_async('eve/CharacterName', {
                'IDs': set(id_list),
            })
        raise ndb.Return(
            self.character_names_from_ids(id_list, api_result=api_result)
        )

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
    def character_ids_from_names_async(self, name_list):
        """Asynchronous version of character_ids_from_names."""
        api_result = yield self.api.get_async(
            'eve/CharacterID', 
            {
                'names': set(name_list),
            }
        )
        raise ndb.Return(
            self.character_ids_from_names(name_list, api_result=api_result)
        )

    @ndb.tasklet
    def character_id_from_name_async(self, name):
        """Asynchronous version of character_id_from_name."""
        resp = yield self.character_ids_from_names_async([name])
        raise ndb.Return(
            api.APIResult(resp.result.get(name), resp.timestamp, resp.expires)
        )


    @ndb.tasklet
    def character_info_from_id_async(self, char_id):
        """Asynchronous version of character_info_from_id."""
        api_result = yield self.api.get_async(
            'eve/CharacterInfo',
            {
                'characterID': char_id,
            }
        )
        raise ndb.Return(
            self.character_info_from_id(char_id, api_result=api_result)
        )

    
    @ndb.tasklet
    def alliances_async(self):
        """Asynchronous version of alliances."""
        api_result = yield self.api.get_async('eve/AllianceList')
        raise ndb.Return(self.alliances(api_result=api_result))
    
    @ndb.tasklet
    def errors_async(self):
        """Asynchronous version of errors."""
        api_result = yield self.api.get_async('eve/ErrorList')
        raise ndb.Return(self.errors(api_result=api_result))
    
    @ndb.tasklet
    def faction_warfare_stats_async(self):
        """Asynchronous version of faction_warfare_stats."""
        api_result = yield self.api.get_async('eve/FacWarStats')
        raise ndb.Return(self.faction_warfare_stats(api_result=api_result))
    
    @ndb.tasklet
    def skill_tree_async(self):
        """Asynchronous version of skill_tree."""
        api_result = yield self.api.get_async('eve/SkillTree')
        raise ndb.Return(self.skill_tree(api_result=api_result))
    
    @ndb.tasklet
    def reference_types_async(self):
        """Asynchronous version of reference_types."""
        api_result = yield self.api.get_async('eve/RefTypes')
        raise ndb.Return(self.reference_types(api_result=api_result))
    
    @ndb.tasklet
    def faction_warfare_leaderboard_async(self):
        """Asynchronous version of faction_warfare_leaderboard."""
        api_result = yield self.api.get_async('eve/FacWarTopStats')
        raise ndb.Return(
            self.faction_warfare_leaderboard(api_result=api_result)
        )

    @ndb.tasklet
    def conquerable_stations_async(self):
        """Asynchronous version of conquerable_stations."""
        api_result = yield self.api.get_async('eve/ConquerableStationlist')
        raise ndb.Return(self.conquerable_stations(api_result=api_result))
