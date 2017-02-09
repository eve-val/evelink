import collections

from evelink import api, constants
from evelink.parsing.assets import parse_assets
from evelink.parsing.bookmarks import parse_bookmarks
from evelink.parsing.contact_list import parse_contact_list
from evelink.parsing.contract_bids import parse_contract_bids
from evelink.parsing.contract_items import parse_contract_items
from evelink.parsing.contracts import parse_contracts
from evelink.parsing.industry_jobs import parse_industry_jobs
from evelink.parsing.planetary_interactions import parse_planetary_colonies
from evelink.parsing.planetary_interactions import parse_planetary_links
from evelink.parsing.planetary_interactions import parse_planetary_pins
from evelink.parsing.planetary_interactions import parse_planetary_routes
from evelink.parsing.kills import parse_kills
from evelink.parsing.orders import parse_market_orders
from evelink.parsing.wallet_journal import parse_wallet_journal
from evelink.parsing.wallet_transactions import parse_wallet_transactions


class auto_call(api.auto_call):
    """Extends 'evelink.api.auto_call' to add 'Char.char_id' as an api
    request argument.
    """

    def __init__(self, path, map_params=None, **kw):
        map_params = map_params if map_params else {}
        map_params['char_id'] = 'characterID'

        super(auto_call, self).__init__(
            path, prop_to_param=('char_id',), map_params=map_params, **kw
        )


class Char(object):
    """Wrapper around /char/ of the EVE API.

    Note that a valid API key is required.
    """

    def __init__(self, char_id, api):
        self.api = api
        self.char_id = char_id

    @auto_call('char/AssetList', map_params={'flat': 'flat'})
    def assets(self, api_result=None, flat=None):
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

        return api.APIResult(parse_assets(api_result.result), api_result.timestamp, api_result.expires)

    @auto_call('char/Bookmarks')
    def bookmarks(self, api_result=None):
        """Retrieves this character's bookmarks."""
        return api.APIResult(parse_bookmarks(api_result.result), api_result.timestamp, api_result.expires)

    @auto_call('char/ContractBids')
    def contract_bids(self, api_result=None):
        """Lists the latest bids that have been made to any recent auctions."""
        return api.APIResult(parse_contract_bids(api_result.result), api_result.timestamp, api_result.expires)

    @auto_call('char/ContractItems', map_params={'contract_id': 'contractID'})
    def contract_items(self, contract_id, api_result=None):
        """Lists items that a specified contract contains"""
        return api.APIResult(parse_contract_items(api_result.result), api_result.timestamp, api_result.expires)

    @auto_call('char/Contracts', map_params={'contract_id' : 'contractID'})
    def contracts(self, contract_id = None, api_result=None):
        """Returns a record of all contracts for a specified character"""
        return api.APIResult(parse_contracts(api_result.result), api_result.timestamp, api_result.expires)

    @auto_call('char/WalletJournal', map_params={'before_id': 'fromID', 'limit': 'rowCount'})
    def wallet_journal(self, before_id=None, limit=None, api_result=None):
        """Returns a complete record of all wallet activity for a specified character"""
        return api.APIResult(parse_wallet_journal(api_result.result), api_result.timestamp, api_result.expires)

    @auto_call('char/AccountBalance')
    def wallet_info(self, api_result=None):
        """Return a given character's wallet."""
        rowset = api_result.result.find('rowset')
        row = rowset.find('row')
        result = {
            'balance': float(row.attrib['balance']),
            'id': int(row.attrib['accountID']),
            'key': int(row.attrib['accountKey']),
        }
        return api.APIResult(result, api_result.timestamp, api_result.expires)

    def wallet_balance(self):
        """Helper to return just the balance from a given character wallet"""
        api_result = self.wallet_info()
        return api.APIResult(api_result.result['balance'], api_result.timestamp, api_result.expires)

    @auto_call('char/WalletTransactions', map_params={'before_id': 'fromID', 'limit': 'rowCount'})
    def wallet_transactions(self, before_id=None, limit=None, api_result=None):
        """Returns wallet transactions for a character."""
        return api.APIResult(parse_wallet_transactions(api_result.result), api_result.timestamp, api_result.expires)

    @auto_call('char/IndustryJobs')
    def industry_jobs(self, api_result=None):
        """Get a list of jobs for a character (active only)."""
        return api.APIResult(parse_industry_jobs(api_result.result), api_result.timestamp, api_result.expires)

    @auto_call('char/IndustryJobsHistory')
    def industry_jobs_history(self, api_result=None):
        """Get a historical list of industry jobs for a character (active and past)."""
        return api.APIResult(parse_industry_jobs(api_result.result), api_result.timestamp, api_result.expires)

    @auto_call('char/PlanetaryColonies')
    def planetary_colonies(self, api_result=None):
        """Get a list of PI planets for a character."""
        return api.APIResult(parse_planetary_colonies(api_result.result), api_result.timestamp, api_result.expires)

    @auto_call('char/PlanetaryLinks', map_params={'planet_id': 'planetID'})
    def planetary_links(self, planet_id, api_result=None):
        """Get a list of PI links for a character's planet."""
        return api.APIResult(parse_planetary_links(api_result.result), api_result.timestamp, api_result.expires)

    @auto_call('char/PlanetaryPins', map_params={'planet_id': 'planetID'})
    def planetary_pins(self, planet_id, api_result=None):
        """Get a list of PI facilities for a character's planet."""
        return api.APIResult(parse_planetary_pins(api_result.result), api_result.timestamp, api_result.expires)

    @auto_call('char/PlanetaryRoutes', map_params={'planet_id': 'planetID'})
    def planetary_routes(self, planet_id, api_result=None):
        """Get a list of PI routing entries for a character's planet."""
        return api.APIResult(parse_planetary_routes(api_result.result), api_result.timestamp, api_result.expires)

    def planetary_route_map(self, routes, unused_ts=None, unused_exp=None):
        """Given the result of planetary_routes, build a map planetid: [linkid1, linkid2, ...]"""
        result = collections.defaultdict(set)
        for route_id, route in routes.items():
            result[route['source_id']].add(route_id)
            result[route['destination_id']].add(route_id)

        return dict(result)

    @auto_call('char/KillMails', map_params={'before_kill': 'beforeKillID'})
    def kills(self, before_kill=None, api_result=None):
        """Look up recent kills for a character.

        before_kill:
            Optional. Only show kills before this kill id. (Used for paging.)
        """

        return api.APIResult(parse_kills(api_result.result), api_result.timestamp, api_result.expires)

    @auto_call('char/KillLog', map_params={'before_kill': 'beforeKillID'})
    def kill_log(self, before_kill=None, api_result=None):
        """Look up recent kills for a character.

        Note: this method uses the long cache version of the endpoint. If you
              want to use the short cache version (recommended), use kills().

        before_kill:
            Optional. Only show kills before this kill id. (Used for paging.)
        """

        return api.APIResult(parse_kills(api_result.result), api_result.timestamp, api_result.expires)

    @auto_call('char/Notifications')
    def notifications(self, api_result=None):
        """Returns the message headers for notifications."""
        result = {}
        rowset = api_result.result.find('rowset')
        for row in rowset.findall('row'):
            a = row.attrib
            notification_id = int(a['notificationID'])
            result[notification_id] = {
                'id': notification_id,
                'type_id': int(a['typeID']),
                'sender_id': int(a['senderID']),
                'timestamp': api.parse_ts(a['sentDate']),
                'read': a['read'] == '1',
            }

        return api.APIResult(result, api_result.timestamp, api_result.expires)

    @auto_call('char/NotificationTexts', map_params={'notification_ids': 'IDs'})
    def notification_texts(self, notification_ids, api_result=None):
        """Returns the message bodies for notifications."""
        result = {}
        rowset = api_result.result.find('rowset')
        for row in rowset.findall('row'):
            notification_id = int(row.attrib['notificationID'])
            notification = {'id': notification_id}
            notification.update(api.parse_keyval_data(row.text))
            result[notification_id] = notification

        missing_ids = api_result.result.find('missingIDs')
        if missing_ids is not None:
            for missing_id in missing_ids.text.split(","):
                result[missing_id] = None

        return api.APIResult(result, api_result.timestamp, api_result.expires)

    @auto_call('char/Standings')
    def standings(self, api_result=None):
        """Returns the standings towards a character from NPC entities."""
        result = {}
        rowsets = {}
        for rowset in api_result.result.find('characterNPCStandings').findall('rowset'):
            rowsets[rowset.attrib['name']] = rowset

        _name_map = {
            'agents': 'agents',
            'corps': 'NPCCorporations',
            'factions': 'factions',
        }

        for key, rowset_name in _name_map.items():
            result[key] = {}
            for row in rowsets[rowset_name].findall('row'):
                a = row.attrib
                from_id = int(a['fromID'])
                result[key][from_id] = {
                    'id': from_id,
                    'name': a['fromName'],
                    'standing': float(a['standing']),
                }

        return api.APIResult(result, api_result.timestamp, api_result.expires)

    @auto_call('char/Skills')
    def skills(self, api_result=None):
        """Returns a specific character's skills."""
        _str, _int, _float, _bool, _ts = api.elem_getters(api_result.result)

        result = {
            'free_skillpoints': _int('freeSkillPoints'),
        }

        rowsets = {}
        for rowset in api_result.result.findall('rowset'):
            key = rowset.attrib['name']
            rowsets[key] = rowset

        result['skills'] = {}
        result['skillpoints'] = 0
        for skill in rowsets['skills']:
            a = skill.attrib
            skill_id = int(a['typeID'])
            sp = int(a['skillpoints'])
            result['skills'][skill_id] = {
                'id': skill_id,
                'skillpoints': sp,
                'level': int(a['level']),
                'published': a['published'] == '1',
            }
            result['skillpoints'] += sp

        return api.APIResult(result, api_result.timestamp, api_result.expires)

    @auto_call('char/Clones')
    def clones(self, api_result=None):
        """Returns jumpclones for a specific character."""
        _str, _int, _float, _bool, _ts = api.elem_getters(api_result.result)
        result = {
            'create_ts': _ts('DoB'),
            'race': _str('race'),
            'bloodline': _str('bloodLine'),
            'ancestry': _str('ancestry'),
            'remote_station_ts': _ts('remoteStationDate'),
            'last_respec_ts': _ts('lastRespecDate'),
            'last_timed_respec_ts': _ts('lastTimedRespec'),
            'free_respecs': _int('freeRespecs'),
            'gender': _str('gender'),
            'attributes': {},
            'implants': {},
            'jumpclone': {
                'jump_ts': _ts('cloneJumpDate'),
            },
        }

        for attr in ('intelligence', 'memory', 'charisma', 'perception', 'willpower'):
            result['attributes'][attr] = {}
            base = int(api_result.result.findtext('attributes/%s' % attr))
            result['attributes'][attr]['base'] = base

        rowsets = {}
        for rowset in api_result.result.findall('rowset'):
            key = rowset.attrib['name']
            rowsets[key] = rowset

        for implant in rowsets['implants']:
            a = implant.attrib
            result['implants'][int(a['typeID'])] = a['typeName']

        jumpclone_implants = {}
        for implant in rowsets['jumpCloneImplants']:
            a = implant.attrib
            jumpclone_id = int(a['jumpCloneID'])
            implants = jumpclone_implants.setdefault(jumpclone_id, {})
            implants[int(a['typeID'])] = a['typeName']

        result['jumpclone']['clones'] = {}
        for jumpclone in rowsets['jumpClones']:
            a = jumpclone.attrib
            jumpclone_id = int(a['jumpCloneID'])
            location_id = int(a['locationID'])
            # This is keyed off location_id because it simplifies a
            # common lookup ("what systems do I have jumpclones in")
            result['jumpclone']['clones'][location_id] = {
                'id': jumpclone_id,
                'name': a['cloneName'],
                'type_id': int(a['typeID']),
                'location_id': location_id,
                'implants': jumpclone_implants.get(jumpclone_id, {})
            }

        return api.APIResult(result, api_result.timestamp, api_result.expires)

    @auto_call('char/CharacterSheet')
    def character_sheet(self, api_result=None):
        """Returns attributes relating to a specific character."""
        _str, _int, _float, _bool, _ts = api.elem_getters(api_result.result)
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
            'balance': _float('balance'),
            'attributes': {},
            'implants': {},
            'jump': {
                'activation_ts': _ts('jumpActivation'),
                'fatigue_ts': _ts('jumpFatigue'),
                'last_update_ts': _ts('jumpLastUpdate'),
            },
            'remote_station_ts': _ts('remoteStationDate'),
            'last_respec_ts': _ts('lastRespecDate'),
            'last_timed_respec_ts': _ts('lastTimedRespec'),
            'free_respecs': _int('freeRespecs'),
            'free_skillpoints': _int('freeSkillPoints'),
            'home_station_id': _int('homeStationID'),
            'jumpclone': {
                'jump_ts': _ts('cloneJumpDate'),
            },
        }

        for attr in ('intelligence', 'memory', 'charisma', 'perception', 'willpower'):
            result['attributes'][attr] = {}
            base = int(api_result.result.findtext('attributes/%s' % attr))
            result['attributes'][attr]['base'] = base

            # NOTE: Removed due to the deprecation of the attribute enhancers section.
            # Better to break things which rely on this field than return the base.
            #
            #result['attributes'][attr]['total'] = base

            # NOTE: CCP has deprecated this in favor of listing the implant typeIDs
            #       as seen below in the 'implants' section.
            #
            #bonus = api_result.result.find('attributeEnhancers/%sBonus' % attr)
            #if bonus is not None:
            #    mod = int(bonus.findtext('augmentatorValue'))
            #    result['attributes'][attr]['total'] += mod
            #    result['attributes'][attr]['bonus'] = {
            #        'name': bonus.findtext('augmentatorName'),
            #        'value': mod,
            #    }

        rowsets = {}
        for rowset in api_result.result.findall('rowset'):
            key = rowset.attrib['name']
            rowsets[key] = rowset

        for implant in rowsets['implants']:
            a = implant.attrib
            result['implants'][int(a['typeID'])] = a['typeName']

        jumpclone_implants = {}
        for implant in rowsets['jumpCloneImplants']:
            a = implant.attrib
            jumpclone_id = int(a['jumpCloneID'])
            implants = jumpclone_implants.setdefault(jumpclone_id, {})
            implants[int(a['typeID'])] = a['typeName']

        result['jumpclone']['clones'] = {}
        for jumpclone in rowsets['jumpClones']:
            a = jumpclone.attrib
            jumpclone_id = int(a['jumpCloneID'])
            location_id = int(a['locationID'])
            # This is keyed off location_id because it simplifies a
            # common lookup ("what systems do I have jumpclones in")
            result['jumpclone']['clones'][location_id] = {
                'id': jumpclone_id,
                'name': a['cloneName'],
                'type_id': int(a['typeID']),
                'location_id': location_id,
                'implants': jumpclone_implants.get(jumpclone_id, {})
            }


        result['skills'] = {}
        result['skillpoints'] = 0
        for skill in rowsets['skills']:
            a = skill.attrib
            skill_id = int(a['typeID'])
            sp = int(a['skillpoints'])
            result['skills'][skill_id] = {
                'id': skill_id,
                'skillpoints': sp,
                'level': int(a['level']),
                'published': a['published'] == '1',
            }
            result['skillpoints'] += sp

        result['roles'] = {}
        for our_role, ccp_role in constants.Char().corp_roles.items():
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

        return api.APIResult(result, api_result.timestamp, api_result.expires)

    @auto_call('char/ContactList')
    def contacts(self, api_result=None):
        """Return a character's personal, corp and alliance contact lists."""
        return api.APIResult(parse_contact_list(api_result.result), api_result.timestamp, api_result.expires)

    @auto_call('char/MarketOrders')
    def orders(self, api_result=None):
        """Return a given character's buy and sell orders."""
        return api.APIResult(parse_market_orders(api_result.result), api_result.timestamp, api_result.expires)

    @auto_call('char/Research')
    def research(self, api_result=None):
        """Returns information about the agents with whom the character is doing research."""
        rowset = api_result.result.find('rowset')
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

        return api.APIResult(result, api_result.timestamp, api_result.expires)

    @auto_call('char/SkillInTraining')
    def current_training(self, api_result=None):
        """Returns the skill that is currently being trained by a specified character"""
        _str, _int, _float, _bool, _ts = api.elem_getters(api_result.result)
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

        return api.APIResult(result, api_result.timestamp, api_result.expires)

    @auto_call('char/SkillQueue')
    def skill_queue(self, api_result=None):
        """returns the skill queue of the character"""
        rowset = api_result.result.find('rowset')
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

        return api.APIResult(result, api_result.timestamp, api_result.expires)

    @auto_call('char/MailMessages')
    def messages(self, api_result=None):
        """Returns a list of headers for a character's mail."""
        rowset = api_result.result.find('rowset')
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

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    @auto_call('char/MailBodies', map_params={'message_ids': 'ids'})
    def message_bodies(self, message_ids, api_result=None):
        """Returns the actual body content of a set of mail messages.

        NOTE: You *must* have recently looked up the headers of
        any messages you are requesting bodies for (via the 'messages'
        method) or else this call will fail.
        """

        rowset = api_result.result.find('rowset')
        results = {}
        for row in rowset.findall('row'):
            message_id = int(row.attrib['messageID'])
            results[message_id] = row.text

        missing_set = api_result.result.find('missingMessageIDs')
        if missing_set is not None:
            missing_ids = [int(i) for i in missing_set.text.split(',')]
            for missing_id in missing_ids:
                results[missing_id] = None

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    @auto_call('char/MailingLists')
    def mailing_lists(self, api_result=None):
        """Returns the mailing lists to which a character is subscribed."""
        rowset = api_result.result.find('rowset')
        results = {}
        for row in rowset.findall('row'):
            a = row.attrib
            results[int(a['listID'])] = a['displayName']

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    @auto_call('char/UpcomingCalendarEvents')
    def calendar_events(self, api_result=None):
        """Returns the list of upcoming calendar events for a character."""
        results = {}
        rowset = api_result.result.find('rowset')
        for row in rowset.findall('row'):
            a = row.attrib
            event = {
                'id': int(a['eventID']),
                'owner': {
                    'id': int(a['ownerID']),
                    'name': a['ownerName'] or None,
                },
                'start_ts': api.parse_ts(a['eventDate']),
                'title': a['eventTitle'],
                'duration': int(a['duration']),
                'important': a['importance'] == '1',
                'description': a['eventText'],
                'response': a['response'],
            }
            results[event['id']] = event

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    @auto_call('char/CalendarEventAttendees', map_params={'event_ids': 'eventIDs'})
    def calendar_attendees(self, event_ids, api_result=None):
        """Returns the list of attendees for the specified calendar event.

        This function takes a list of event IDs and returns a dict of dicts,
        with the top-level dict being keyed by event ID and the children
        keyed by the character IDs of the attendees.

        NOTE: You must have recently fetched the list of calendar events
        (using the 'calendar_events' method) before calling this method.
        """

        results = dict((int(i),{}) for i in event_ids)
        rowset = api_result.result.find('rowset')
        for row in rowset.findall('row'):
            a = row.attrib
            attendee = {
                'id': int(a['characterID']),
                'name': a['characterName'],
                'response': a['response'],
            }
            results[int(a['eventID'])][attendee['id']] = attendee

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    def event_attendees(self, event_id, api_result=None):
        """Returns the attendees for a single event.

        (This is a convenience wrapper around 'calendar_attendees'.)

        NOTE: You must have recently fetched the list of calendar events
        (using the 'calendar_events' method) before calling this method.
        """

        api_result = self.calendar_attendees([event_id])
        return api.APIResult(api_result.result[int(event_id)], api_result.timestamp, api_result.expires)

    @auto_call('char/FacWarStats')
    def faction_warfare_stats(self, api_result=None):
        """Returns FW stats for this character, if enrolled in FW.

        NOTE: This will return an error instead if the character
        is not enrolled in Faction Warfare.

        """
        _str, _int, _float, _bool, _ts = api.elem_getters(api_result.result)

        result = {
            'faction': {
                'id': _int('factionID'),
                'name': _str('factionName'),
            },
            'enlist_ts': _ts('enlisted'),
            'rank': {
                'current': _int('currentRank'),
                'highest': _int('highestRank'),
            },
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
        }

        return api.APIResult(result, api_result.timestamp, api_result.expires)

    @auto_call('char/Medals')
    def medals(self, api_result=None):
        """Returns a list of medals the character has."""
        result = {'current': {}, 'other': {}}
        _map = {
            'currentCorporation': 'current',
            'otherCorporations': 'other',
        }

        for rowset in api_result.result.findall('rowset'):
            name = _map[rowset.attrib['name']]
            for row in rowset.findall('row'):
                a = row.attrib
                medal_id = int(a['medalID'])
                result[name][medal_id] = {
                    'id': medal_id,
                    'reason': a['reason'],
                    'public': a['status'] == 'public',
                    'issuer_id': int(a['issuerID']),
                    'corp_id': int(a['corporationID']),
                    'title': a['title'],
                    'description': a['description'],
                }

        return api.APIResult(result, api_result.timestamp, api_result.expires)

    @auto_call('char/ContactNotifications')
    def contact_notifications(self, api_result=None):
        """Returns pending contact notifications."""
        results = {}
        rowset = api_result.result.find('rowset')
        for row in rowset.findall('row'):
            a = row.attrib
            note = {
                'id': int(a['notificationID']),
                'sender': {
                    'id': int(a['senderID']),
                    'name': a['senderName'],
                },
                'timestamp': api.parse_ts(a['sentDate']),
                'data': api.parse_keyval_data(a['messageData']),
            }
            results[note['id']] = note

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    @auto_call('char/Locations', map_params={'location_list': 'IDs'})
    def locations(self, location_list, api_result=None):
        rowset = api_result.result.find('rowset')
        rows = rowset.findall('row')

        results = {}
        for row in rows:
            name = row.attrib['itemName'] or None
            id = int(row.attrib['itemID']) or None
            x = float(row.attrib['x']) or None
            y = float(row.attrib['y']) or None
            z = float(row.attrib['z']) or None

            results[id] = {
                'name': name,
                'id' : id,
                'x' : x,
                'y' : y,
                'z' : z,
            }
        return api.APIResult(results, api_result.timestamp, api_result.expires)

    @auto_call('char/Blueprints')
    def blueprints(self, api_result=None):
        rowset = api_result.result.find('rowset')
        rows = rowset.findall('row')

        results = {}
        for row in rows:
            results[int(row.attrib['itemID'])] = {
                'location_id': int(row.attrib['locationID']),
                'type_id': int(row.attrib['typeID']),
                'type_name': row.attrib['typeName'],
                'location_flag': int(row.attrib['flagID']),
                'quantity': int(row.attrib['quantity']),
                'time_efficiency': int(row.attrib['timeEfficiency']),
                'material_efficiency': int(row.attrib['materialEfficiency']),
                'runs': int(row.attrib['runs']),
            }

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    @auto_call('char/ChatChannels')
    def chat_channels(self, api_result=None):
        """Get a list of chat channels this character owns or ops."""
        rowset = api_result.result.find('rowset')

        results = {}
        for row in rowset.findall('row'):
            a = row.attrib
            channel = {
                'id': int(a['channelID']),
                'owner': {
                    'id': int(a['ownerID']),
                    'name': a['ownerName'],
                },
                'name': a['displayName'],
                'comparison_name': a['comparisonKey'],
                'passworded': a['hasPassword'] == 'True',
                'motd': a['motd'],
                'allowed': {},
                'blocked': {},
                'muted': {},
                'ops': {},
            }

            sections = {}
            for section in row.findall('rowset'):
                sections[section.attrib['name']] = section

            if 'allowed' in sections:
                for entity in sections['allowed'].findall('row'):
                    entity_id = int(entity.attrib['accessorID'])
                    channel['allowed'][entity_id] = {
                        'id': entity_id,
                        'name': entity.attrib['accessorName'],
                    }
            if 'blocked' in sections:
                for entity in sections['blocked'].findall('row'):
                    entity_id = int(entity.attrib['accessorID'])
                    channel['blocked'][entity_id] = {
                        'id': entity_id,
                        'name': entity.attrib['accessorName'],
                        'until_ts': api.parse_ts(entity.attrib['untilWhen']),
                        'reason': entity.attrib['reason'],
                    }
            if 'muted' in sections:
                for entity in sections['muted'].findall('row'):
                    entity_id = int(entity.attrib['accessorID'])
                    channel['muted'][entity_id] = {
                        'id': entity_id,
                        'name': entity.attrib['accessorName'],
                        'until_ts': api.parse_ts(entity.attrib['untilWhen']),
                        'reason': entity.attrib['reason'],
                    }
            if 'operators' in sections:
                for entity in sections['operators'].findall('row'):
                    entity_id = int(entity.attrib['accessorID'])
                    channel['ops'][entity_id] = {
                        'id': entity_id,
                        'name': entity.attrib['accessorName'],
                    }

            results[channel['id']] = channel

        return api.APIResult(results, api_result.timestamp, api_result.expires)


# vim: set ts=4 sts=4 sw=4 et:
