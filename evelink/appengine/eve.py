from google.appengine.ext import ndb

from evelink import api, eve
from evelink.appengine.api import auto_gae_api

class EVE(eve.EVE):
    """Wrapper around /eve/ of the EVE API."""

    @auto_gae_api
    def __init__(self, api=None):
        self.api = api

    @ndb.tasklet
    def certificate_tree_async(self):
        """Returns a list of certificates in eve."""
        api_result = yield self.api.get_async('eve/CertificateTree')
        raise ndb.Return(self.certificate_tree(api_result=api_result))
        
    @ndb.tasklet
    def character_names_from_ids_async(self, id_list):
        """Retrieve a dict mapping character IDs to names.

        id_list:
            A list of ids to retrieve names.

        NOTE: *ALL* character IDs passed to this function
        must be valid - an invalid character ID will cause
        the entire call to fail.
        """

        api_result = yield self.api.get_async('eve/CharacterName', {
                'IDs': set(id_list),
            })
        raise ndb.Return(
            self.character_names_from_ids(id_list, api_result=api_result)
        )

    @ndb.tasklet
    def character_name_from_id_async(self, char_id):
        """Retrieve the character's name based on ID.

        Convenience wrapper around character_names_from_ids().
        """
        resp = yield self.character_names_from_ids_async([char_id])
        raise ndb.Return(
            api.APIResult(
                resp.result.get(char_id), resp.timestamp, resp.expires
            )
        )

    @ndb.tasklet
    def character_ids_from_names_async(self, name_list):
        """Retrieve a dict mapping character names to IDs.

        name_list:
            A list of names to retrieve character IDs.

        Names of unknown characters will map to None.
        """

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
        """Retrieve the named character's ID.

        Convenience wrapper around character_ids_from_names().
        """
        resp = yield self.character_ids_from_names_async([name])
        raise ndb.Return(
            api.APIResult(resp.result.get(name), resp.timestamp, resp.expires)
        )


    @ndb.tasklet
    def character_info_from_id_async(self, char_id):
        """Retrieve a dict of info about the designated character."""

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
        """Return a dict of all alliances in EVE."""

        api_result = yield self.api.get_async('eve/AllianceList')
        raise ndb.Return(self.alliances(api_result=api_result))
    
    @ndb.tasklet
    def errors_async(self):
        """Return a mapping of error codes to messages."""

        api_result = yield self.api.get_async('eve/ErrorList')
        raise ndb.Return(self.errors(api_result=api_result))
    
    @ndb.tasklet
    def faction_warfare_stats_async(self):
        """Return various statistics from Faction Warfare."""

        api_result = yield self.api.get_async('eve/FacWarStats')
        raise ndb.Return(self.faction_warfare_stats(api_result=api_result))
    
    @ndb.tasklet
    def skill_tree_async(self):
        """Return a dict of all available skill groups."""

        api_result = yield self.api.get_async('eve/SkillTree')
        raise ndb.Return(self.skill_tree(api_result=api_result))
    
    @ndb.tasklet
    def reference_types_async(self):
        """Return a dict containing id -> name reference type mappings."""

        api_result = yield self.api.get_async('eve/RefTypes')
        raise ndb.Return(self.reference_types(api_result=api_result))
    
    @ndb.tasklet
    def faction_warfare_leaderboard_async(self):
        """Return top-100 lists from Faction Warfare."""

        api_result = yield self.api.get_async('eve/FacWarTopStats')
        raise ndb.Return(
            self.faction_warfare_leaderboard(api_result=api_result)
        )

    @ndb.tasklet
    def conquerable_stations_async(self):

        api_result = yield self.api.get_async('eve/ConquerableStationlist')
        raise ndb.Return(self.conquerable_stations(api_result=api_result))
