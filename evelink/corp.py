from evelink import api, constants
from evelink.parsing.assets import parse_assets
from evelink.parsing.contact_list import parse_contact_list
from evelink.parsing.contract_bids import parse_contract_bids
from evelink.parsing.contract_items import parse_contract_items
from evelink.parsing.contracts import parse_contracts
from evelink.parsing.industry_jobs import parse_industry_jobs
from evelink.parsing.kills import parse_kills
from evelink.parsing.orders import parse_market_orders
from evelink.parsing.wallet_journal import parse_wallet_journal
from evelink.parsing.wallet_transactions import parse_wallet_transactions

class Corp(object):
    """Wrapper around /corp/ of the EVE API.

    Note that a valid corp API key is required.
    """

    def __init__(self, api):
        self.api = api

    def corporation_sheet(self, corp_id=None):
        """Get information about a corporation.

        NOTE: This method may be called with or without specifying
        a corporation ID. If a corporation ID is specified, the public
        information for that corporation will be returned, and no api
        key is necessary. If a corporation ID is *not* specified,
        a corp api key *must* be provided, and the private information
        for that corporation will be returned along with the public info.
        """
        params = {}
        if corp_id is not None:
            params['corporationID'] = corp_id

        api_result = self.api.get("corp/CorporationSheet", params)

        def get_logo_details(logo_result):
            _str, _int, _float, _bool, _ts = api.elem_getters(logo_result)
            return {
                'graphic_id': _int('graphicID'),
                'shapes': [
                    {'id': _int('shape1'), 'color': _int('color1')},
                    {'id': _int('shape2'), 'color': _int('color2')},
                    {'id': _int('shape3'), 'color': _int('color3')},
                ],
            }

        _str, _int, _float, _bool, _ts = api.elem_getters(api_result.result)

        result = {
            'id': _int('corporationID'),
            'name': _str('corporationName'),
            'ticker': _str('ticker'),
            'ceo': {
                'id': _int('ceoID'),
                'name': _str('ceoName'),
            },
            'hq': {
                'id': _int('stationID'),
                'name': _str('stationName'),
            },
            'description': _str('description'),
            'url': _str('url'),
            'alliance': {
                'id': _int('allianceID') or None,
                'name': _str('allianceName') or None,
            },
            'tax_percent': _float('taxRate'),
            'members': {
                'current': _int('memberCount'),
            },
            'shares': _int('shares'),
            'logo': get_logo_details(api_result.result.find('logo')),
        }

        if corp_id is None:
            result['members']['limit'] = _int('memberLimit')

            rowsets = dict((r.attrib['name'], r) for r in api_result.result.findall('rowset'))

            division_types = {
                'hangars': 'divisions',
                'wallets': 'walletDivisions',
            }

            for key, rowset_name in division_types.iteritems():
                divisions = {}
                for row in rowsets[rowset_name].findall('row'):
                    a = row.attrib
                    divisions[int(a['accountKey'])] = a['description']

                result[key] = divisions

        return api.APIResult(result, api_result.timestamp, api_result.expires)

    def industry_jobs(self):
        """Get a list of jobs for a corporation."""

        api_result = self.api.get('corp/IndustryJobs')

        return api.APIResult(parse_industry_jobs(api_result.result), api_result.timestamp, api_result.expires)

    def npc_standings(self):
        """Returns information about the corporation's standings towards NPCs.

        NOTE: This is *only* NPC standings. Player standings are accessed
        via the 'contacts' method.
        """
        api_result = self.api.get('corp/Standings')
        container = api_result.result.find('corporationNPCStandings')

        rowsets = dict((r.attrib['name'], r) for r in container.findall('rowset'))
        results = {
            'agents': {},
            'corps': {},
            'factions': {},
        }

        _standing_types = {
            'agents': 'agents',
            'corps': 'NPCCorporations',
            'factions': 'factions',
        }

        for key, rowset_name in _standing_types.iteritems():
            for row in rowsets[rowset_name].findall('row'):
                a = row.attrib
                standing = {
                    'id': int(a['fromID']),
                    'name': a['fromName'],
                    'standing': float(a['standing']),
                }
                results[key][standing['id']] = standing

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    def kills(self, before_kill=None):
        """Look up recent kills for a corporation.

        before_kill:
            Optional. Only show kills before this kill id. (Used for paging.)
        """

        params = {}
        if before_kill is not None:
            params['beforeKillID'] = before_kill
        api_result = self.api.get('corp/KillLog', params)

        return api.APIResult(parse_kills(api_result.result), api_result.timestamp, api_result.expires)

    def wallet_info(self):
        """Get information about corp wallets."""

        api_result = self.api.get('corp/AccountBalance')

        rowset = api_result.result.find('rowset')
        results = {}
        for row in rowset.findall('row'):
            wallet = {
                'balance': float(row.attrib['balance']),
                'id': int(row.attrib['accountID']),
                'key': int(row.attrib['accountKey']),
            }
            results[wallet['key']] = wallet

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    def wallet_journal(self, before_id=None, limit=None):
        """Returns wallet journal for a corporation."""

        params = {}
        if before_id is not None:
            params['fromID'] = before_id
        if limit is not None:
            params['rowCount'] = limit
        api_result = self.api.get('corp/WalletJournal', params)

        return api.APIResult(parse_wallet_journal(api_result.result), api_result.timestamp, api_result.expires)

    def wallet_transactions(self, before_id=None, limit=None):
        """Returns wallet transactions for a corporation."""

        params = {}
        if before_id is not None:
            params['fromID'] = before_id
        if limit is not None:
            params['rowCount'] = limit
        api_result = self.api.get('corp/WalletTransactions', params)

        return api.APIResult(parse_wallet_transactions(api_result.result), api_result.timestamp, api_result.expires)

    def orders(self):
        """Return a corporation's buy and sell orders."""
        api_result = self.api.get('corp/MarketOrders')

        return api.APIResult(parse_market_orders(api_result.result), api_result.timestamp, api_result.expires)

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
        api_result = self.api.get('corp/AssetList')
        return api.APIResult(parse_assets(api_result.result), api_result.timestamp, api_result.expires)

    def faction_warfare_stats(self):
        """Returns stats from faction warfare if this corp is enrolled.

        NOTE: This will raise an APIError if the corp is not enrolled in
        Faction Warfare.
        """
        api_result = self.api.get('corp/FacWarStats')

        _str, _int, _float, _bool, _ts = api.elem_getters(api_result.result)

        result = {
            'faction': {
                'id': _int('factionID'),
                'name': _str('factionName'),
            },
            'start_ts': _ts('enlisted'),
            'pilots': _int('pilots'),
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

    def contract_bids(self):
        """Lists the latest bids that have been made to any recent auctions."""
        api_result = self.api.get('corp/ContractBids')

        return api.APIResult(parse_contract_bids(api_result.result), api_result.timestamp, api_result.expires)

    def contract_items(self, contract_id):
        """Lists items that a specified contract contains"""
        api_result = self.api.get('corp/ContractItems', {'contractID': contract_id})

        return api.APIResult(parse_contract_items(api_result.result), api_result.timestamp, api_result.expires)

    def contracts(self):
        """Get information about corp contracts."""
        api_result = self.api.get('corp/Contracts')
        return api.APIResult(parse_contracts(api_result.result), api_result.timestamp, api_result.expires)

    def shareholders(self):
        """Get information about a corp's shareholders."""
        api_result = self.api.get('corp/Shareholders')

        results = {
            'char': {},
            'corp': {},
        }
        rowsets = dict((r.attrib['name'], r) for r in api_result.result.findall('rowset'))

        for row in rowsets['characters'].findall('row'):
            a = row.attrib
            holder = {
                'id': int(a['shareholderID']),
                'name': a['shareholderName'],
                'corp': {
                    'id': int(a['shareholderCorporationID']),
                    'name': a['shareholderCorporationName'],
                },
                'shares': int(a['shares']),
            }
            results['char'][holder['id']] = holder

        for row in rowsets['corporations'].findall('row'):
            a = row.attrib
            holder = {
                'id': int(a['shareholderID']),
                'name': a['shareholderName'],
                'shares': int(a['shares']),
            }
            results['corp'][holder['id']] = holder

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    def contacts(self):
        """Return the corp's corp and alliance contact lists."""
        api_result = self.api.get('corp/ContactList')
        return api.APIResult(parse_contact_list(api_result.result), api_result.timestamp, api_result.expires)

    def titles(self):
        """Returns information about the corporation's titles."""
        api_result = self.api.get('corp/Titles')

        rowset = api_result.result.find('rowset')
        results = {}
        for row in rowset.findall('row'):
            a = row.attrib
            title = {
                'id': int(a['titleID']),
                'name': a['titleName'],
                'roles': {},
                'can_grant': {},
            }
            rowsets = dict((r.attrib['name'], r) for r in row.findall('rowset'))

            def get_roles(rowset_name):
                roles = {}
                for role_row in rowsets[rowset_name].findall('row'):
                    ra = role_row.attrib
                    role = {
                        'id': int(ra['roleID']),
                        'name': ra['roleName'],
                        'description': ra['roleDescription'],
                    }
                    roles[role['id']] = role
                return roles

            for key, rowset_name in constants.Corp.role_types.iteritems():
                roles = get_roles(rowset_name)
                title['roles'][key] = roles

            for key, rowset_name in constants.Corp.grantable_types.iteritems():
                roles = get_roles(rowset_name)
                title['can_grant'][key] = roles

            results[title['id']] = title

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    def starbases(self):
        """Returns information about the corporation's POSes."""
        api_result = self.api.get('corp/StarbaseList')

        rowset = api_result.result.find('rowset')
        results = {}
        for row in rowset.findall('row'):
            a = row.attrib
            starbase = {
                'id': int(a['itemID']),
                'type_id': int(a['typeID']),
                'location_id': int(a['locationID']),
                'moon_id': int(a['moonID']),
                'state': constants.Corp.pos_states[int(a['state'])],
                'state_ts': api.parse_ts(a['stateTimestamp']),
                'online_ts': api.parse_ts(a['onlineTimestamp']),
                'standings_owner_id': int(a['standingOwnerID']),
            }
            results[starbase['id']] = starbase

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    def starbase_details(self, starbase_id):
        """Returns details about the specified POS."""
        api_result = self.api.get('corp/StarbaseDetail', {'itemID': starbase_id})

        _str, _int, _float, _bool, _ts = api.elem_getters(api_result.result)

        general_settings = api_result.result.find('generalSettings')
        combat_settings = api_result.result.find('combatSettings')

        def get_fuel_bay_perms(settings):
            # Two 2-bit fields
            usage_flags = int(settings.find('usageFlags').text)
            take_value = usage_flags % 4
            view_value = (usage_flags >> 2) % 4
            return {
                'view': constants.Corp.pos_permission_entities[view_value],
                'take': constants.Corp.pos_permission_entities[take_value],
            }

        def get_deploy_perms(settings):
            # Four 2-bit fields
            deploy_flags = int(settings.find('deployFlags').text)
            anchor_value = (deploy_flags >> 6) % 4
            unanchor_value = (deploy_flags >> 4) % 4
            online_value = (deploy_flags >> 2) % 4
            offline_value = deploy_flags % 4
            return {
                'anchor': constants.Corp.pos_permission_entities[anchor_value],
                'unanchor': constants.Corp.pos_permission_entities[unanchor_value],
                'online': constants.Corp.pos_permission_entities[online_value],
                'offline': constants.Corp.pos_permission_entities[offline_value],
            }

        def get_combat_settings(settings):
            result = {
                'standings_owner_id': int(settings.find('useStandingsFrom').attrib['ownerID']),
                'hostility': {},
            }

            hostility = result['hostility']

            # TODO(ayust): The fields returned by the API don't completely match up with
            # the fields available in-game. May want to revisit this in the future.

            standing = settings.find('onStandingDrop')
            hostility['standing'] = {
                'threshold': float(standing.attrib['standing']) / 100,
                'enabled': standing.attrib.get('enabled') != '0',
            }

            sec_status = settings.find('onStatusDrop')
            hostility['sec_status'] = {
                'threshold': float(sec_status.attrib['standing']) / 100,
                'enabled': sec_status.attrib.get('enabled') != '0',
            }

            hostility['aggression'] = {
                'enabled': settings.find('onAggression').get('enabled') != '0',
            }

            hostility['war'] = {
                'enabled': settings.find('onCorporationWar').get('enabled') != '0',
            }

            return result

        result = {
            'state': constants.Corp.pos_states[_int('state')],
            'state_ts': _ts('stateTimestamp'),
            'online_ts': _ts('onlineTimestamp'),
            'permissions': {
                'fuel': get_fuel_bay_perms(general_settings),
                'deploy': get_deploy_perms(general_settings),
                'forcefield': {
                    'corp': general_settings.find('allowCorporationMembers').text == '1',
                    'alliance': general_settings.find('allowAllianceMembers').text == '1',
                },
            },
            'combat': get_combat_settings(combat_settings),
            'fuel': {},
        }

        rowset = api_result.result.find('rowset')
        for row in rowset.findall('row'):
            a = row.attrib
            result['fuel'][int(a['typeID'])] = int(a['quantity'])

        return api.APIResult(result, api_result.timestamp, api_result.expires)

    def members(self, extended=True):
        """Returns details about each member of the corporation."""
        args = {}
        if extended:
            args['extended'] = 1
        api_result = self.api.get('corp/MemberTracking', args)

        rowset = api_result.result.find('rowset')
        results = {}
        for row in rowset.findall('row'):
            a = row.attrib
            member = {
                'id': int(a['characterID']),
                'name': a['name'],
                'join_ts': api.parse_ts(a['startDateTime']),
                'base': {
                    # TODO(aiiane): Maybe remove this?
                    # It doesn't seem to ever have a useful value.
                    'id': int(a['baseID']),
                    'name': a['base'],
                },
                # Note that title does not include role titles,
                # only ones like 'CEO'
                'title': a['title'],
            }
            if extended:
                member.update({
                    'logon_ts': api.parse_ts(a['logonDateTime']),
                    'logoff_ts': api.parse_ts(a['logoffDateTime']),
                    'location': {
                        'id': int(a['locationID']),
                        'name': a['location'],
                    },
                    'ship_type': {
                        # "Not available" = -1 ship id; we change to None
                        'id': max(int(a['shipTypeID']), 0) or None,
                        'name': a['shipType'] or None,
                    },
                    'roles': int(a['roles']),
                    'can_grant': int(a['grantableRoles']),
                })

            results[member['id']] = member

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    def permissions(self):
        """Returns information about corporation member permissions."""
        api_result = self.api.get('corp/MemberSecurity')

        results = {}
        rowset = api_result.result.find('rowset')
        for row in rowset.findall('row'):
            a = row.attrib
            member = {
                'id': int(a['characterID']),
                'name': a['name'],
                'titles': {},
            }

            rowsets = dict((r.attrib['name'], r) for r in row.findall('rowset'))

            for title_row in rowsets['titles'].findall('row'):
                a = title_row.attrib
                member['titles'][int(a['titleID'])] = a['titleName']

            def get_roleset(roles_dict):
                roles_group = {}
                for key, rowset_name in roles_dict.iteritems():
                    roles = {}
                    roles_rowset = rowsets[rowset_name]
                    for role_row in roles_rowset.findall('row'):
                        a = role_row.attrib
                        roles[int(a['roleID'])] = a['roleName']
                    roles_group[key] = roles
                return roles_group

            member['roles'] = get_roleset(constants.Corp.role_types)
            member['can_grant'] = get_roleset(constants.Corp.grantable_types)

            results[member['id']] = member

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    def permissions_log(self):
        """Returns information about changes to member permissions."""
        api_result = self.api.get('corp/MemberSecurityLog')

        inverse_role_types = dict((v,k) for k,v in constants.Corp.role_types.iteritems())

        results = []
        rowset = api_result.result.find('rowset')
        for row in rowset.findall('row'):
            a = row.attrib
            change = {
                'timestamp': api.parse_ts(a['changeTime']),
                'recipient': {
                    'id': int(a['characterID']),
                    'name': a['characterName'],
                },
                'issuer': {
                    'id': int(a['issuerID']),
                    'name': a['issuerName'],
                },
                'role_type': inverse_role_types[a['roleLocationType']],
                'roles': {
                    'before': {},
                    'after': {},
                },
            }

            rowsets = dict((r.attrib['name'], r) for r in row.findall('rowset'))
            old, new = change['roles']['before'], change['roles']['after']

            for role_row in rowsets['oldRoles'].findall('row'):
                a = role_row.attrib
                old[int(a['roleID'])] = a['roleName']

            for role_row in rowsets['newRoles'].findall('row'):
                a = role_row.attrib
                new[int(a['roleID'])] = a['roleName']

            results.append(change)

        results.sort(key=lambda r: r['timestamp'], reverse=True)
        return api.APIResult(results, api_result.timestamp, api_result.expires)

    def stations(self):
        """Returns information about the corporation's (non-POS) stations."""
        api_result = self.api.get('corp/OutpostList')

        rowset = api_result.result.find('rowset')
        results = {}
        for row in rowset.findall('row'):
            a = row.attrib
            station = {
                'id': int(a['stationID']),
                'owner_id': int(a['ownerID']),
                'name': a['stationName'],
                'system_id': int(a['solarSystemID']),
                'docking_fee_per_volume': float(a['dockingCostPerShipVolume']),
                'office_fee': int(a['officeRentalCost']),
                'type_id': int(a['stationTypeID']),
                'reprocessing': {
                    'efficiency': float(a['reprocessingEfficiency']),
                    'cut': float(a['reprocessingStationTake']),
                },
                'standing_owner_id': int(a['standingOwnerID']),
            }
            results[station['id']] = station

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    def station_services(self, station_id):
        """Returns information about a given station's services."""
        api_result = self.api.get('corp/OutpostServiceDetail', {'itemID': station_id})

        rowset = api_result.result.find('rowset')
        results = {}
        for row in rowset.findall('row'):
            a = row.attrib
            service = {
                'name': a['serviceName'],
                'owner_id': int(a['ownerID']),
                'standing': {
                    'minimum': float(a['minStanding']),
                    'bad_surcharge': float(a['surchargePerBadStanding']),
                    'good_discount': float(a['discountPerGoodStanding']),
                },
            }
            results[service['name']] = service

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    def medals(self):
        """Returns information about the medals created by a corporation."""
        api_result = self.api.get('corp/Medals')

        rowset = api_result.result.find('rowset')
        results = {}
        for row in rowset.findall('row'):
            a = row.attrib
            medal = {
                'id': int(a['medalID']),
                'creator_id': int(a['creatorID']),
                'title': a['title'],
                'description': a['description'],
                'create_ts': api.parse_ts(a['created']),
            }
            results[medal['id']] = medal

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    def member_medals(self):
        """Returns information about medals assigned to corporation members."""
        api_result = self.api.get("corp/MemberMedals")

        rowset = api_result.result.find('rowset')
        results = {}
        for row in rowset.findall('row'):
            a = row.attrib
            award = {
                'medal_id': int(a['medalID']),
                'char_id': int(a['characterID']),
                'reason': a['reason'],
                'public': a['status'] == 'public',
                'issuer_id': int(a['issuerID']),
                'timestamp': api.parse_ts(a['issued']),
            }
            results.setdefault(award['char_id'], {})[award['medal_id']] = award

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    def container_log(self):
        """Returns a log of actions performed on corporation containers."""
        api_result = self.api.get("corp/ContainerLog")

        results = []
        rowset = api_result.result.find('rowset')

        def int_or_none(val):
            return int(val) if val else None

        for row in rowset.findall('row'):
            a = row.attrib
            action = {
                'timestamp': api.parse_ts(a['logTime']),
                'item': {
                    'id': int(a['itemID']),
                    'type_id': int(a['itemTypeID']),
                },
                'actor': {
                    'id': int(a['actorID']),
                    'name': a['actorName'],
                },
                'location_id': int(a['locationID']),
                'action': a['action'],
                'details': {
                    # TODO(aiiane): Find a translation for this flag field
                    'flag': int(a['flag']),
                    'password_type': a['passwordType'] or None,
                    'type_id': int_or_none(a['typeID']),
                    'quantity': int_or_none(a['quantity']),
                    'config': {
                        'old': int_or_none(a['oldConfiguration']),
                        'new': int_or_none(a['newConfiguration']),
                    },
                },
            }
            results.append(action)

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    def locations(self, location_list):
        params={
            'IDs' : location_list,
        }
        api_result = self.api.get('corp/Locations', params)

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



# vim: set ts=4 sts=4 sw=4 et:
