from evelink import api

class EVE(object):
    """Wrapper around /eve/ of the EVE API."""

    @api.auto_api
    def __init__(self, api=None):
        self.api = api

    @api.auto_call('eve/CharacterName', map_params={'id_list': 'IDs'})
    def character_names_from_ids(self, id_list, api_result=None):
        """Retrieve a dict mapping character IDs to names.

        id_list:
            A list of ids to retrieve names.

        NOTE: *ALL* character IDs passed to this function
        must be valid - an invalid character ID will cause
        the entire call to fail.
        """

        if api_result is None:
            # The API doesn't actually tell us which character IDs are invalid
            msg = "One or more of these character IDs are invalid: %r"
            raise ValueError(msg % id_list)

        rowset = api_result.result.find('rowset')
        rows = rowset.findall('row')

        results = {}
        for row in rows:
            name = row.attrib['name']
            char_id = int(row.attrib['characterID'])
            results[char_id] = name

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    def character_name_from_id(self, char_id):
        """Retrieve the character's name based on ID.

        Convenience wrapper around character_names_from_ids().
        """
        api_result = self.character_names_from_ids([char_id])
        return api.APIResult(api_result.result.get(int(char_id)), api_result.timestamp, api_result.expires)

    @api.auto_call('eve/CharacterID', map_params={'name_list': 'names'})
    def character_ids_from_names(self, name_list, api_result=None):
        """Retrieve a dict mapping character names to IDs.

        name_list:
            A list of names to retrieve character IDs.

        Names of unknown characters will map to None.
        """

        rowset = api_result.result.find('rowset')
        rows = rowset.findall('row')

        results = {}
        for row in rows:
            name = row.attrib['name']
            char_id = int(row.attrib['characterID']) or None
            results[name] = char_id

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    def character_id_from_name(self, name):
        """Retrieve the named character's ID.

        Convenience wrapper around character_ids_from_names().
        """
        api_result = self.character_ids_from_names([name])
        return api.APIResult(list(api_result.result.values())[0], api_result.timestamp, api_result.expires)

    @api.auto_call('eve/CharacterAffiliation', map_params={'id_list': 'ids'})
    def affiliations_for_characters(self, id_list, api_result=None):
        """Retrieve the affiliations for a set of character IDs, returned as a dictionary.

        name_list:
            A list of names to retrieve IDs for.

        IDs for anything not a character will be returned with a name, but nothing else.
        """

        rowset = api_result.result.find('rowset')
        rows = rowset.findall('row')

        results = {}
        for row in rows:
            char_id = int(row.attrib['characterID'])
            char_name = row.attrib['characterName']
            corp_id = int(row.attrib['corporationID']) or None
            corp_name = row.attrib['corporationName'] or None
            faction_id = int(row.attrib['factionID']) or None
            faction_name = row.attrib['factionName'] or None
            alliance_id = int(row.attrib['allianceID']) or None
            alliance_name = row.attrib['allianceName'] or None
            results[char_id] = {
                'id': char_id,
                'name': char_name,
                'corp': {
                    'id': corp_id,
                    'name': corp_name
                }
            }

            if faction_id is not None:
                results[char_id]['faction'] = {
                    'id': faction_id,
                    'name': faction_name
                }

            if alliance_id is not None:
                results[char_id]['alliance'] = {
                    'id': alliance_id,
                    'name': alliance_name
                }

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    def affiliations_for_character(self, char_id):
        """Retrieve the affiliations of a single character

        Convenience wrapper around owner_ids_from_names().
        """

        api_result = self.affiliations_for_characters([char_id])
        return api.APIResult(api_result.result[char_id], api_result.timestamp, api_result.expires)

    @api.auto_call('eve/CharacterInfo', map_params={'char_id': 'characterID'})
    def character_info_from_id(self, char_id, api_result=None):
        """Retrieve a dict of info about the designated character."""
        if api_result is None:
            raise ValueError("Unable to fetch info for character %r" % char_id)

        _str, _int, _float, _bool, _ts = api.elem_getters(api_result.result)

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
        history = api_result.result.find('rowset')
        for row in history.findall('row'):
            corp_id = int(row.attrib['corporationID'])
            corp_name = row.attrib['corporationName']
            start_date = api.parse_ts(row.attrib['startDate'])
            results['history'].append({
                    'corp_id': corp_id,
                    'corp_name': corp_name,
                    'start_ts': start_date,
                })

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    @api.auto_call('eve/AllianceList')
    def alliances(self, api_result=None):
        """Return a dict of all alliances in EVE."""
        results = {}
        rowset = api_result.result.find('rowset')
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

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    @api.auto_call('eve/ErrorList')
    def errors(self, api_result=None):
        """Return a mapping of error codes to messages."""
        rowset = api_result.result.find('rowset')
        results = {}
        for row in rowset.findall('row'):
            code = int(row.attrib['errorCode'])
            message = row.attrib['errorText']
            results[code] = message

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    @api.auto_call('eve/FacWarStats')
    def faction_warfare_stats(self, api_result=None):
        """Return various statistics from Faction Warfare."""
        totals = api_result.result.find('totals')
        rowsets = dict((r.attrib['name'], r) for r in api_result.result.findall('rowset'))

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

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    @api.auto_call('eve/SkillTree')
    def skill_tree(self, api_result=None):
        """Return a dict of all available skill groups."""
        rowset = api_result.result.find('rowset') # skillGroups

        results = {}
        name_cache = {}
        for row in rowset.findall('row'):

            # the skill group data
            g = row.attrib
            group = {
                'id': int(g['groupID']),
                'name': g['groupName'],
                'skills': {}
                }
            # Because :ccp: groups can sometimes be listed
            # multiple times with different skills, and the
            # correct result is to add the contents together
            group = results.get(group['id'], group)

            # now get the actual skill data
            skills_rs = row.find('rowset') # skills
            for skill_row in skills_rs.findall('row'):
                a = skill_row.attrib
                _str, _int, _float, _bool, _ts = api.elem_getters(skill_row)

                req_attrib = skill_row.find('requiredAttributes')

                skill = {
                    'id': int(a['typeID']),
                    'group_id': int(a['groupID']),
                    'name': a['typeName'],
                    'published': (a['published'] == '1'),
                    'description': _str('description'),
                    'rank': _int('rank'),
                    'required_skills': {},
                    'bonuses': {},
                    'attributes': {
                        'primary': api.get_named_value(req_attrib, 'primaryAttribute'),
                        'secondary': api.get_named_value(req_attrib, 'secondaryAttribute'),
                        }
                    }

                name_cache[skill['id']] = skill['name']

                # Check each rowset inside the skill, and branch based on the name attribute
                for sub_rs in skill_row.findall('rowset'):

                    if sub_rs.attrib['name'] == 'requiredSkills':
                        for sub_row in sub_rs.findall('row'):
                            b = sub_row.attrib
                            req = {
                                'level': int(b['skillLevel']),
                                'id': int(b['typeID']),
                                }
                            skill['required_skills'][req['id']] = req

                    elif sub_rs.attrib['name'] == 'skillBonusCollection':
                        for sub_row in sub_rs.findall('row'):
                            b = sub_row.attrib
                            bonus = {
                                'type': b['bonusType'],
                                'value': float(b['bonusValue']),
                                }
                            skill['bonuses'][bonus['type']] = bonus

                group['skills'][skill['id']] = skill

            results[group['id']] = group

        # Second pass to fill in required skill names
        for group in results.values():
            for skill in group['skills'].values():
                for skill_id, skill_info in skill['required_skills'].items():
                    skill_info['name'] = name_cache.get(skill_id)

        return api.APIResult(results, api_result.timestamp, api_result.expires)


    @api.auto_call('eve/RefTypes')
    def reference_types(self, api_result=None):
        """Return a dict containing id -> name reference type mappings."""
        rowset = api_result.result.find('rowset')

        results = {}
        for row in rowset.findall('row'):
            a = row.attrib
            results[int(a['refTypeID'])] = a['refTypeName']

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    @api.auto_call('eve/TypeName', map_params={'id_list': 'IDs'})
    def type_names_from_ids(self, id_list, api_result=None):
        """Return a dict containing id -> name mappings for the supplied type ids."""
        rowset = api_result.result.find('rowset')
        results = {}
        for row in rowset.findall('row'):
            a= row.attrib
            results[int(a['typeID'])] = a['typeName']

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    def type_name_from_id(self, type_id):
        """Retrieve a type name based on ID.

        Convenience wrapper around type_names_from_ids().
        """
        api_result = self.type_names_from_ids([type_id])
        return api.APIResult(api_result.result.get(int(type_id)), api_result.timestamp, api_result.expires)

    @api.auto_call('eve/FacWarTopStats')
    def faction_warfare_leaderboard(self, api_result=None):
        """Return top-100 lists from Faction Warfare."""

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
            'char': parse_section(api_result.result.find('characters'), 'character'),
            'corp': parse_section(api_result.result.find('corporations'), 'corporation'),
            'faction': parse_section(api_result.result.find('factions'), 'faction'),
        }

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    @api.auto_call('eve/ConquerableStationlist')
    def conquerable_stations(self, api_result=None):
        results = {}
        rowset = api_result.result.find('rowset')
        for row in rowset.findall('row'):
            station = {
                'id': int(row.attrib['stationID']),
                'name': row.attrib['stationName'],
                'type_id': int(row.attrib['stationTypeID']),
                'system_id': int(row.attrib['solarSystemID']),
                'corp': {
                    'id': int(row.attrib['corporationID']),
                    'name': row.attrib['corporationName'] },
                'x': float(row.attrib['x']),
                'y': float(row.attrib['y']),
                'z': float(row.attrib['z']),
                }
            results[station['id']] = station

        return api.APIResult(results, api_result.timestamp, api_result.expires)



# vim: set ts=4 sts=4 sw=4 et:
