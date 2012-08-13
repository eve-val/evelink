from evelink import api

class EVE(object):
    """Wrapper around /eve/ of the EVE API."""

    @api.auto_api
    def __init__(self, api=None):
        self.api = api

    def character_names_from_ids(self, id_list):
        """Retrieve a dict mapping character IDs to names.

        id_list:
            A list of ids to retrieve names.

        NOTE: *ALL* character IDs passed to this function
        must be valid - an invalid character ID will cause
        the entire call to fail.
        """

        api_result = self.api.get('eve/CharacterName', {
                'IDs': set(id_list),
            })

        if api_result is None:
            # The API doesn't actually tell us which character IDs are invalid
            msg = "One or more of these character IDs are invalid: %r"
            raise ValueError(msg % id_list)

        rowset = api_result.find('rowset')
        rows = rowset.findall('row')

        results = {}
        for row in rows:
            name = row.attrib['name']
            char_id = int(row.attrib['characterID'])
            results[char_id] = name

        return results

    def character_name_from_id(self, char_id):
        """Retrieve the character's name based on ID.

        Convenience wrapper around character_names_from_ids().
        """
        return self.character_names_from_ids([char_id]).get(char_id)

    def character_ids_from_names(self, name_list):
        """Retrieve a dict mapping character names to IDs.

        name_list:
            A list of names to retrieve character IDs.

        Names of unknown characters will map to None.
        """

        api_result = self.api.get('eve/CharacterID', {
                'names': set(name_list),
            })

        rowset = api_result.find('rowset')
        rows = rowset.findall('row')

        results = {}
        for row in rows:
            name = row.attrib['name']
            char_id = int(row.attrib['characterID']) or None
            results[name] = char_id

        return results

    def character_id_from_name(self, name):
        """Retrieve the named character's ID.

        Convenience wrapper around character_ids_from_names().
        """
        return self.character_ids_from_names([name]).get(name)

    def character_info_from_id(self, char_id):
        """Retrieve a dict of info about the designated character."""

        api_result = self.api.get('eve/CharacterInfo', {
                'characterID': char_id,
            })

        if api_result is None:
            raise ValueError("Unable to fetch info for character %r" % char_id)

        _str, _int, _float, _bool, _ts = api.elem_getters(api_result)

        results = {
            'id': _int('characterID'),
            'name': _str('characterName'),
            'race': _str('race'),
            'bloodline': _str('bloodline'),
            'sec_status': _float('securityStatus'),
            'skillpoints': _int('skillPoints'),
            'location': _str('lastKnownLocation'),
            'isk': _float('accountBalance'),

            'corp': {
                'id': _int('corporationID'),
                'name': _str('corporation'),
                'timestamp': _ts('corporationDate'),
            },

            'alliance': {
                'id': _int('allianceID'),
                'name': _str('alliance'),
                'timestamp': _ts('allianceDate'),
            },

            'ship': {
                'name': _str('shipName'),
                'type_id': _int('shipTypeID'),
                'type_name': _str('shipTypeName'),
            },
            
            'history': [],
        }

        # Add in corp history
        history = api_result.find('rowset')
        for row in history.findall('row'):
            corp_id = int(row.attrib['corporationID'])
            start_date = api.parse_ts(row.attrib['startDate'])
            results['history'].append({
                    'corp_id': corp_id,
                    'start_ts': start_date,
                })

        return results

    def alliances(self):
        """Return a dict of all alliances in EVE."""

        api_result = self.api.get('eve/AllianceList')

        results = {}
        rowset = api_result.find('rowset')
        for row in rowset.findall('row'):
            alliance = {
                'name': row.attrib['name'],
                'ticker': row.attrib['shortName'],
                'id': int(row.attrib['allianceID']),
                'executor_id': int(row.attrib['executorCorpID']),
                'member_count': int(row.attrib['memberCount']),
                'timestamp': api.parse_ts(row.attrib['startDate']),
                'member_corps': {},
            }

            corp_rowset = row.find('rowset')
            for corp_row in corp_rowset.findall('row'):
                corp_id = int(corp_row.attrib['corporationID'])
                corp_ts = api.parse_ts(corp_row.attrib['startDate'])
                alliance['member_corps'][corp_id] = {
                    'id': corp_id,
                    'timestamp': corp_ts,
                }

            results[alliance['id']] = alliance

        return results

    def errors(self):
        """Return a mapping of error codes to messages."""

        api_result = self.api.get('eve/ErrorList')

        rowset = api_result.find('rowset')
        results = {}
        for row in rowset.findall('row'):
            code = int(row.attrib['errorCode'])
            message = row.attrib['errorText']
            results[code] = message

        return results

    def faction_warfare_stats(self):
        """Return various statistics from Faction Warfare."""

        api_result = self.api.get('eve/FacWarStats')

        totals = api_result.find('totals')
        rowsets = dict((r.attrib['name'], r) for r in api_result.findall('rowset'))

        _str, _int, _float, _bool, _ts = api.elem_getters(totals)
        results = {
            'kills': {
                'yesterday': _int('killsYesterday'),
                'week': _int('killsLastWeek'),
                'total': _int('killsTotal'),
            },
            'points': {
                'yesterday': _int('victoryPointsYesterday'),
                'week': _int('victoryPointsLastWeek'),
                'total': _int('victoryPointsTotal'),
            },
            'factions': {},
            'wars': [],
        }

        for row in rowsets['factions'].findall('row'):
            a = row.attrib
            faction = {
                'id': int(a['factionID']),
                'name': a['factionName'],
                'pilots': int(a['pilots']),
                'systems': int(a['systemsControlled']),
                'kills': {
                    'yesterday': int(a['killsYesterday']),
                    'week': int(a['killsLastWeek']),
                    'total': int(a['killsTotal']),
                },
                'points': {
                    'yesterday': int(a['victoryPointsYesterday']),
                    'week': int(a['victoryPointsLastWeek']),
                    'total': int(a['victoryPointsTotal']),
                },
            }
            results['factions'][faction['id']] = faction

        for row in rowsets['factionWars'].findall('row'):
            a = row.attrib
            war = {
                'faction': {
                    'id': int(a['factionID']),
                    'name': a['factionName'],
                },
                'against': {
                    'id': int(a['againstID']),
                    'name': a['againstName'],
                },
            }
            results['wars'].append(war)

        return results

    def faction_warfare_leaderboard(self):
        """Return top-100 lists from Faction Warfare."""

        api_result = self.api.get('eve/FacWarTopStats')

        def parse_top_100(rowset, prefix, attr, attr_name):
            top100 = []
            id_field = '%sID' % prefix
            name_field = '%sName' % prefix
            for row in rowset.findall('row'):
                a = row.attrib
                top100.append({
                    'id': int(a[id_field]),
                    'name': a[name_field],
                    attr_name: int(a[attr]),
                })
            return top100

        def parse_section(section, prefix):
            section_result = {}
            rowsets = dict((r.attrib['name'], r) for r in section.findall('rowset'))

            section_result['kills'] = {
                'yesterday': parse_top_100(rowsets['KillsYesterday'], prefix, 'kills', 'kills'),
                'week': parse_top_100(rowsets['KillsLastWeek'], prefix, 'kills', 'kills'),
                'total': parse_top_100(rowsets['KillsTotal'], prefix, 'kills', 'kills'),
            }

            section_result['points'] = {
                'yesterday': parse_top_100(rowsets['VictoryPointsYesterday'],
                    prefix, 'victoryPoints', 'points'),
                'week': parse_top_100(rowsets['VictoryPointsLastWeek'],
                    prefix, 'victoryPoints', 'points'),
                'total': parse_top_100(rowsets['VictoryPointsTotal'],
                    prefix, 'victoryPoints', 'points'),
            }

            return section_result

        results = {
            'char': parse_section(api_result.find('characters'), 'character'),
            'corp': parse_section(api_result.find('corporations'), 'corporation'),
            'faction': parse_section(api_result.find('factions'), 'faction'),
        }
        
        return results
        
    def conquerable_stations(self):
        
        api_result = api.get('eve/ConquerableStationlist')
        
        results = {}
        rowset = api_result.find('rowset')
        for row in rowset.findall('row'):
            station = {
                'id': int(row.attrib['stationID']),
                'name': row.attrib['stationName'],
                'type_id': int(row.attrib['stationTypeID']),
                'system_id': int(row.attrib['solarSystemID']),
                corp = {
                    'id': int(row.attrib['corporationID']),
                    'name': row.attrib['corporationName'] }
                }
            results[station['id']] = station
            
        return(results)
