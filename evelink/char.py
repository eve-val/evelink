from evelink import api, constants
from evelink.parsing.assets import parse_assets
from evelink.parsing.contracts import parse_contracts
from evelink.parsing.industry_jobs import parse_industry_jobs
from evelink.parsing.orders import parse_market_orders

class Char(object):
    """Wrapper around /char/ of the EVE API.

    Note that a valid API key is required.
    """

    def __init__(self, char_id, api):
        self.api = api
        self.char_id = char_id

    def assets(self):
        """Get information about corp assets.

        Each item is a dict, with keys 'id', 'item_type_id',
        'quantity', 'location_id', 'location_flag', and 'packaged'.
        'location_flag' denotes additional information about the
        item's location; see
        http://wiki.eve-id.net/API_Inventory_Flags for more details.

        If the item corresponds to a container, it will have a key
        'contents', which is itself a list of items in the same format
        (potentially recursively holding containers of its own).  If
        the contents do not have 'location_id's of their own, they
        inherit the 'location_id' of their parent container, for
        convenience.

        At the top level, the result is a dict mapping location ID
        (typically a solar system) to a dict containing a 'contents'
        key, which maps to a list of items.  That is, you can think of
        the top-level values as "containers" with no fields except for
        "contents" and "location_id".
        """
        api_result = self.api.get('char/AssetList',
            {'characterID': self.char_id})

        return parse_assets(api_result)

    def contracts(self):
        """Returns a record of all contracts for a specified character"""
        api_result = self.api.get('char/Contracts',
            {'characterID': self.char_id})
        return parse_contracts(api_result)

    def wallet_journal(self, before_id=None, limit=None):
        """Returns a complete record of all wallet activity for a specified character"""
        params = {'characterID': self.char_id}
        if before_id is not None:
            params['fromID'] = before_id
        if limit is not None:
            params['rowCount'] = limit
        api_result = self.api.get('char/WalletJournal', params)

        rowset = api_result.find('rowset')
        result = []

        for row in rowset.findall('row'):
            a = row.attrib
            entry = {
                'timestamp': api.parse_ts(a['date']),
                'id': int(a['refID']),
                'type_id': int(a['refTypeID']),
                'party_1': {
                    'name': a['ownerName1'],
                    'id': int(a['ownerID1']),
                },
                'party_2': {
                    'name': a['ownerName2'],
                    'id': int(a['ownerID2']),
                },
                'arg': {
                    'name': a['argName1'],
                    'id': int(a['argID1']),
                },
                'amount': float(a['amount']),
                'balance': float(a['balance']),
                'reason': a['reason'],
                'tax': {
                    'taxer_id': int(a['taxReceiverID'] or 0),
                    'amount': float(a['taxAmount'] or 0),
                },
            }

            result.append(entry)

        result.sort(key=lambda x: x['id'])
        return result

    def wallet_info(self):
        """Return a given character's wallet."""
        api_result = self.api.get('char/AccountBalance',
            {'characterID': self.char_id})

        rowset = api_result.find('rowset')
        row = rowset.find('row')
        result = {
            'balance': float(row.attrib['balance']),
            'id': int(row.attrib['accountID']),
            'key': int(row.attrib['accountKey']),
        }
        return result

    def wallet_balance(self):
        """Helper to return just the balance from a given character wallet"""

        return self.wallet_info()['balance']

    def industry_jobs(self):
        """Get a list of jobs for a character"""

        api_result = self.api.get('char/IndustryJobs',
            {'characterID': self.char_id})

        return parse_industry_jobs(api_result)

    def kills(self, before_kill=None):
        """Look up recent kills for the given character

        before_kill:
            Optional. Only show kills before this kill id. (Used for paging.)
        """

        params = {'characterID': self.char_id}
        if before_kill is not None:
            params['beforeKillID'] = before_kill
        api_result = self.api.get('char/KillLog', params)

        rowset = api_result.find('rowset')
        result = {}
        for row in rowset.findall('row'):
            a = row.attrib
            kill_id = int(a['killID'])
            result[kill_id] = {
                'id': kill_id,
                'system_id': int(a['solarSystemID']),
                'time': api.parse_ts(a['killTime']),
                'moon_id': int(a['moonID']),
            }

            victim = row.find('victim')
            a = victim.attrib
            result[kill_id]['victim'] = {
                'id': int(a['characterID']),
                'name': a['characterName'],
                'corp': {
                    'id': int(a['corporationID']),
                    'name': a['corporationName'],
                },
                'alliance': {
                    'id': int(a['allianceID']),
                    'name': a['allianceName'],
                },
                'faction': {
                    'id': int(a['factionID']),
                    'name': a['factionName'],
                },
                'damage': int(a['damageTaken']),
                'ship_type_id': int(a['shipTypeID']),
            }

            result[kill_id]['attackers'] = {}

            rowsets = {}
            for rowset in row.findall('rowset'):
                key = rowset.attrib['name']
                rowsets[key] = rowset

            for attacker in rowsets['attackers'].findall('row'):
                a = attacker.attrib
                attacker_id = int(a['characterID'])
                result[kill_id]['attackers'][attacker_id] = {
                    'id': attacker_id,
                    'name': a['characterName'],
                    'corp': {
                        'id': int(a['corporationID']),
                        'name': a['corporationName'],
                    },
                    'alliance': {
                        'id': int(a['allianceID']),
                        'name': a['allianceName'],
                    },
                    'faction': {
                        'id': int(a['factionID']),
                        'name': a['factionName'],
                    },
                    'sec_status': float(a['securityStatus']),
                    'damage': int(a['damageDone']),
                    'final_blow': a['finalBlow'] == '1',
                    'weapon_type_id': int(a['weaponTypeID']),
                    'ship_type_id': int(a['shipTypeID']),
                }

            result[kill_id]['items'] = {}
            for item in rowsets['items'].findall('row'):
                a = item.attrib
                type_id = int(a['typeID'])
                result[kill_id]['items'][type_id] = {
                    'id': type_id,
                    'flag': int(a['flag']),
                    'dropped': int(a['qtyDropped']),
                    'destroyed': int(a['qtyDestroyed']),
                }

        return result

    def character_sheet(self):
        """Returns attributes relating to a specific character."""
        api_result = self.api.get('char/CharacterSheet',
            {'characterID': self.char_id})

        _str, _int, _float, _bool, _ts = api.elem_getters(api_result)
        result = {
            'id': _int('characterID'),
            'name': _str('name'),
            'create_ts': _ts('DoB'),
            'race': _str('race'),
            'bloodline': _str('bloodLine'),
            'ancestry': _str('ancestry'),
            'gender': _str('gender'),
            'corp': {
                'id': _int('corporationID'),
                'name': _str('corporationName'),
            },
            'alliance': {
                'id': _int('allianceID') or None,
                'name': _str('allianceName'),
            },
            'clone': {
                'name': _str('cloneName'),
                'skillpoints': _int('cloneSkillPoints'),
            },
            'balance': _float('balance'),
            'attributes': {},
        }

        for attr in ('intelligence', 'memory', 'charisma', 'perception', 'willpower'):
            result['attributes'][attr] = {}
            base = int(api_result.findtext('attributes/%s' % attr))
            result['attributes'][attr]['base'] = base
            result['attributes'][attr]['total'] = base
            bonus = api_result.find('attributeEnhancers/%sBonus' % attr)
            if bonus is not None:
                mod = int(bonus.findtext('augmentatorValue'))
                result['attributes'][attr]['total'] += mod
                result['attributes'][attr]['bonus'] = {
                    'name': bonus.findtext('augmentatorName'),
                    'value': mod,
                }

        rowsets = {}
        for rowset in api_result.findall('rowset'):
            key = rowset.attrib['name']
            rowsets[key] = rowset

        result['skills'] = []
        result['skillpoints'] = 0
        for skill in rowsets['skills']:
            a = skill.attrib
            sp = int(a['skillpoints'])
            result['skills'].append({
                'id': int(a['typeID']),
                'skillpoints': sp,
                'level': int(a['level']),
                'published': a['published'] == '1',
            })
            result['skillpoints'] += sp

        result['certificates'] = set()
        for cert in rowsets['certificates']:
            result['certificates'].add(int(cert.attrib['certificateID']))

        result['roles'] = {}
        for our_role, ccp_role in constants.Char().corp_roles.iteritems():
            result['roles'][our_role] = {}
            for role in rowsets[ccp_role]:
                a = role.attrib
                role_id = int(a['roleID'])
                result['roles'][our_role][role_id] = {
                    'id': role_id,
                    'name': a['roleName'],
                }

        result['titles'] = {}
        for title in rowsets['corporationTitles']:
            a = title.attrib
            title_id = int(a['titleID'])
            result['titles'][title_id] = {
                'id': title_id,
                'name': a['titleName'],
            }

        return result

    def orders(self):
        """Return a given character's buy and sell orders."""
        api_result = self.api.get('char/MarketOrders',
            {'characterID': self.char_id})

        return parse_market_orders(api_result)

    def research(self):
        """Returns information about the agents with whom the character is doing research."""

        api_result = self.api.get('char/Research',
            {'characterID': self.char_id})

        rowset = api_result.find('rowset')
        rows = rowset.findall('row')
        result = {}
        for row in rows:
            a = row.attrib
            id = int(a['agentID'])
            result[id] = {
                'id': id,
                'skill_id': int(a['skillTypeID']),
                'timestamp': api.parse_ts(a['researchStartDate']),
                'per_day': float(a['pointsPerDay']),
                'remaining': float(a['remainderPoints']),
            }

        return result

    def current_training(self):
        """Returns the skill that is currently being trained by a specified character"""

        api_result = self.api.get('char/SkillInTraining',
            {'characterID': self.char_id})

        _str, _int, _float, _bool, _ts = api.elem_getters(api_result)
        result = {
            'start_ts': _ts('trainingStartTime'),
            'end_ts': _ts('trainingEndTime'),
            'type_id': _int('trainingTypeID'),
            'start_sp': _int('trainingStartSP'),
            'end_sp': _int('trainingDestinationSP'),
            'current_ts': _ts('currentTQTime'),
            'level': _int('trainingToLevel'),
            'active': _bool('skillInTraining'),
        }

        return result

    def skill_queue(self):
        """returns the skill queue of the character"""
        api_result = self.api.get('char/SkillQueue',
            {'characterID': self.char_id})

        rowset = api_result.find('rowset')
        rows = rowset.findall('row')
        result = []
        for row in rows:
            a = row.attrib
            line = {
                'position': int(a['queuePosition']),
                'type_id': int(a['typeID']),
                'level': int(a['level']),
                'start_sp': int(a['startSP']),
                'end_sp': int(a['endSP']),
                'start_ts': api.parse_ts(a['startTime']),
                'end_ts': api.parse_ts(a['endTime']),
            }

            result.append(line)

        return result

    def messages(self):
        """Returns a list of headers for a character's mail."""
        api_result = self.api.get('char/MailMessages',
            {'characterID': self.char_id})

        rowset = api_result.find('rowset')
        results = []
        for row in rowset.findall('row'):
            a = row.attrib
            message = {
                'id': int(a['messageID']),
                'sender_id': int(a['senderID']),
                'timestamp': api.parse_ts(a['sentDate']),
                'title': a['title'],
                'to': {},
            }

            org_id = a['toCorpOrAllianceID']
            message['to']['org_id'] = int(org_id) if org_id else None

            char_ids = a['toCharacterIDs']
            message['to']['char_ids'] = [int(i) for i in char_ids.split(',')] if char_ids else None

            list_ids = a['toListID']
            message['to']['list_ids'] = [int(i) for i in list_ids.split(',')] if list_ids else None

            results.append(message)

        return results
