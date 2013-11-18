from evelink import api

class EVE(object):
    """Wrapper around /eve/ of the EVE API."""

    @api.auto_api
    def __init__(self, api=None):
        self.api = api

    def certificate_tree(self):
        """Returns a list of certificates in eve."""
        api_result = self.api.get('eve/CertificateTree')

        result = {}
        rowset = api_result.result.find('rowset')
        categories = rowset.findall('row')

        for category in categories:
            cat_attr = category.attrib
            cat_name = cat_attr['categoryName']
            cat_tree = {
                'name': cat_name,
                'id': int(cat_attr['categoryID']),
                'classes': {},
            }

            cls_rowset = category.find('rowset')
            classes = cls_rowset.findall('row')
            for cls in classes:
                cls_attr = cls.attrib
                cls_name = cls_attr['className']
                cls_def = {
                    'name': cls_name,
                    'id': int(cls_attr['classID']),
                    'certificates': {}
                }

                cert_rowset = cls.find('rowset')
                certificates = cert_rowset.findall('row')
                for cert in certificates:
                    cert_attr = cert.attrib
                    cert_id = int(cert_attr['certificateID'])
                    cert_entry = {
                      'id': cert_id,
                      'grade': int(cert_attr['grade']),
                      'corp_id': int(cert_attr['corporationID']),
                      'description': cert_attr['description'],
                      'required_skills': {},
                      'required_certs': {}
                    }

                    req_rowsets = {}
                    for rowset in cert.findall('rowset'):
                      req_rowsets[rowset.attrib['name']] = rowset

                    req_skills = req_rowsets['requiredSkills'].findall('row')
                    for skill in req_skills:
                        cert_entry['required_skills'][
                          int(skill.attrib['typeID'])
                        ] = int(skill.attrib['level'])

                    req_certs = req_rowsets['requiredCertificates'].findall('row')
                    for req_cert in req_certs:
                        cert_entry['required_certs'][
                          int(req_cert.attrib['certificateID'])
                        ] = int(req_cert.attrib['grade'])


                    cls_def['certificates'][cert_id] = cert_entry

                cat_tree['classes'][cls_name] = cls_def

            result[cat_name] = cat_tree

        return api.APIResult(result, api_result.timestamp, api_result.expires)

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
        return api.APIResult(api_result.result.get(char_id), api_result.timestamp, api_result.expires)

    def character_ids_from_names(self, name_list):
        """Retrieve a dict mapping character names to IDs.

        name_list:
            A list of names to retrieve character IDs.

        Names of unknown characters will map to None.
        """

        api_result = self.api.get('eve/CharacterID', {
                'names': set(name_list),
            })

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
        return api.APIResult(api_result.result.get(name), api_result.timestamp, api_result.expires)

    def character_info_from_id(self, char_id):
        """Retrieve a dict of info about the designated character."""

        api_result = self.api.get('eve/CharacterInfo', {
                'characterID': char_id,
            })

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
            start_date = api.parse_ts(row.attrib['startDate'])
            results['history'].append({
                    'corp_id': corp_id,
                    'start_ts': start_date,
                })

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    def alliances(self):
        """Return a dict of all alliances in EVE."""

        api_result = self.api.get('eve/AllianceList')

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

    def errors(self):
        """Return a mapping of error codes to messages."""

        api_result = self.api.get('eve/ErrorList')

        rowset = api_result.result.find('rowset')
        results = {}
        for row in rowset.findall('row'):
            code = int(row.attrib['errorCode'])
            message = row.attrib['errorText']
            results[code] = message

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    def faction_warfare_stats(self):
        """Return various statistics from Faction Warfare."""

        api_result = self.api.get('eve/FacWarStats')

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

    def skill_tree(self):
        """Return a dict of all available skill groups."""

        api_result = self.api.get('eve/SkillTree')

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
        for group in results.itervalues():
            for skill in group['skills'].itervalues():
                for skill_id, skill_info in skill['required_skills'].iteritems():
                    skill_info['name'] = name_cache.get(skill_id)

        return api.APIResult(results, api_result.timestamp, api_result.expires)


    def reference_types(self):
        """Return a dict containing id -> name reference type mappings."""

        api_result = self.api.get('eve/RefTypes')
        rowset = api_result.result.find('rowset')

        results = {}
        for row in rowset.findall('row'):
            a = row.attrib
            results[int(a['refTypeID'])] = a['refTypeName']

        return api.APIResult(results, api_result.timestamp, api_result.expires)

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
            'char': parse_section(api_result.result.find('characters'), 'character'),
            'corp': parse_section(api_result.result.find('corporations'), 'corporation'),
            'faction': parse_section(api_result.result.find('factions'), 'faction'),
        }

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    def conquerable_stations(self):

        api_result = self.api.get('eve/ConquerableStationlist')

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
                    'name': row.attrib['corporationName'] }
                }
            results[station['id']] = station

        return api.APIResult(results, api_result.timestamp, api_result.expires)



# vim: set ts=4 sts=4 sw=4 et:
