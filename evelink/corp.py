from evelink import api, constants
from evelink.parsing.assets import parse_assets
from evelink.parsing.bookmarks import parse_bookmarks
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

    @api.auto_call('corp/CorporationSheet', map_params={'corp_id': 'corporationID'})
    def corporation_sheet(self, corp_id=None, api_result=None):
        """Get information about a corporation.

        NOTE: This method may be called with or without specifying
        a corporation ID. If a corporation ID is specified, the public
        information for that corporation will be returned, and no api
        key is necessary. If a corporation ID is *not* specified,
        a corp api key *must* be provided, and the private information
        for that corporation will be returned along with the public info.
        """

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

            for key, rowset_name in division_types.items():
                divisions = {}
                for row in rowsets[rowset_name].findall('row'):
                    a = row.attrib
                    divisions[int(a['accountKey'])] = a['description']

                result[key] = divisions

        return api.APIResult(result, api_result.timestamp, api_result.expires)

    @api.auto_call('corp/IndustryJobs')
    def industry_jobs(self, api_result=None):
        """Get a list of jobs for a corporation (active only)."""
        return api.APIResult(parse_industry_jobs(api_result.result), api_result.timestamp, api_result.expires)

    @api.auto_call('corp/IndustryJobsHistory')
    def industry_jobs_history(self, api_result=None):
        """Get the industry job history for a corporation (active and past)."""
        return api.APIResult(parse_industry_jobs(api_result.result), api_result.timestamp, api_result.expires)

    @api.auto_call('corp/Standings')
    def npc_standings(self, api_result=None):
        """Returns information about the corporation's standings towards NPCs.

        NOTE: This is *only* NPC standings. Player standings are accessed
        via the 'contacts' method.
        """

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

        for key, rowset_name in _standing_types.items():
            for row in rowsets[rowset_name].findall('row'):
                a = row.attrib
                standing = {
                    'id': int(a['fromID']),
                    'name': a['fromName'],
                    'standing': float(a['standing']),
                }
                results[key][standing['id']] = standing

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    @api.auto_call('corp/KillMails', map_params={'before_kill': 'beforeKillID'})
    def kills(self, before_kill=None, api_result=None):
        """Look up recent kills for a corporation.

        before_kill:
            Optional. Only show kills before this kill id. (Used for paging.)
        """

        return api.APIResult(parse_kills(api_result.result), api_result.timestamp, api_result.expires)

    @api.auto_call('corp/KillLog', map_params={'before_kill': 'beforeKillID'})
    def kill_log(self, before_kill=None, api_result=None):
        """Look up recent kills for a corporation.

        Note: this method uses the long cache version of the endpoint. If you
              want to use the short cache version (recommended), use kills().

        before_kill:
            Optional. Only show kills before this kill id. (Used for paging.)
        """

        return api.APIResult(parse_kills(api_result.result), api_result.timestamp, api_result.expires)

    @api.auto_call('corp/AccountBalance')
    def wallet_info(self, api_result=None):
        """Get information about corp wallets."""
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

    @api.auto_call('corp/WalletJournal', map_params={'before_id': 'fromID', 'limit': 'rowCount', 'account': 'accountKey'})
    def wallet_journal(self, before_id=None, limit=None, account=None, api_result=None):
        """Returns wallet journal for a corporation."""
        return api.APIResult(parse_wallet_journal(api_result.result), api_result.timestamp, api_result.expires)

    @api.auto_call('corp/WalletTransactions', map_params={'before_id': 'fromID', 'limit': 'rowCount', 'account': 'accountKey'})
    def wallet_transactions(self, before_id=None, limit=None, account=None, api_result=None):
        """Returns wallet transactions for a corporation."""
        return api.APIResult(parse_wallet_transactions(api_result.result), api_result.timestamp, api_result.expires)

    @api.auto_call('corp/MarketOrders')
    def orders(self, api_result=None):
        """Return a corporation's buy and sell orders."""
        return api.APIResult(parse_market_orders(api_result.result), api_result.timestamp, api_result.expires)

    @api.auto_call('corp/AssetList', map_params={'flat': 'flat'})
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

    @api.auto_call('corp/Bookmarks')
    def bookmarks(self, api_result=None):
        """Retrieves this corp's bookmarks."""
        return api.APIResult(parse_bookmarks(api_result.result), api_result.timestamp, api_result.expires)

    @api.auto_call('corp/FacWarStats')
    def faction_warfare_stats(self, api_result=None):
        """Returns stats from faction warfare if this corp is enrolled.

        NOTE: This will raise an APIError if the corp is not enrolled in
        Faction Warfare.
        """

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

    @api.auto_call('corp/ContractBids')
    def contract_bids(self, api_result=None):
        """Lists the latest bids that have been made to any recent auctions."""
        return api.APIResult(parse_contract_bids(api_result.result), api_result.timestamp, api_result.expires)

    @api.auto_call('corp/ContractItems', map_params={'contract_id': 'contractID'})
    def contract_items(self, contract_id, api_result=None):
        """Lists items that a specified contract contains"""
        return api.APIResult(parse_contract_items(api_result.result), api_result.timestamp, api_result.expires)

    @api.auto_call('corp/Contracts', map_params={'contract_id' : 'contractID'})
    def contracts(self, contract_id = None, api_result=None):
        """Get information about corp contracts."""
        return api.APIResult(parse_contracts(api_result.result), api_result.timestamp, api_result.expires)

    @api.auto_call('corp/Shareholders')
    def shareholders(self, api_result=None):
        """Get information about a corp's shareholders."""
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

    @api.auto_call('corp/ContactList')
    def contacts(self, api_result=None):
        """Return the corp's corp and alliance contact lists."""
        return api.APIResult(parse_contact_list(api_result.result), api_result.timestamp, api_result.expires)

    @api.auto_call('corp/Titles')
    def titles(self, api_result=None):
        """Returns information about the corporation's titles."""
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

            for key, rowset_name in constants.Corp.role_types.items():
                roles = get_roles(rowset_name)
                title['roles'][key] = roles

            for key, rowset_name in constants.Corp.grantable_types.items():
                roles = get_roles(rowset_name)
                title['can_grant'][key] = roles

            results[title['id']] = title

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    @api.auto_call('corp/StarbaseList')
    def starbases(self, api_result=None):
        """Returns information about the corporation's POSes."""
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

    @api.auto_call('corp/StarbaseDetail', map_params={'starbase_id': 'itemID'})
    def starbase_details(self, starbase_id, api_result=None):
        """Returns details about the specified POS."""
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

    def members(self, extended=True, api_result=None):
        """Returns details about each member of the corporation."""
        if api_result is None:
            args = {}
            if extended:
                args['extended'] = 1
            api_result = self.api.get('corp/MemberTracking', params=args)

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

    @api.auto_call('corp/MemberSecurity')
    def permissions(self, api_result=None):
        """Returns information about corporation member permissions."""
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
                for key, rowset_name in roles_dict.items():
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

    @api.auto_call('corp/MemberSecurityLog')
    def permissions_log(self, api_result=None):
        """Returns information about changes to member permissions."""
        inverse_role_types = dict((v,k) for k,v in constants.Corp.role_types.items())

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

    @api.auto_call('corp/OutpostList')
    def stations(self, api_result=None):
        """Returns information about the corporation's (non-POS) stations."""
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
                'x': float(a['x']),
                'y': float(a['y']),
                'z': float(a['z']),
            }
            results[station['id']] = station

        return api.APIResult(results, api_result.timestamp, api_result.expires)

    @api.auto_call('corp/OutpostServiceDetail', map_params={'station_id': 'itemID'})
    def station_services(self, station_id, api_result=None):
        """Returns information about a given station's services."""
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

    @api.auto_call('corp/Medals')
    def medals(self, api_result=None):
        """Returns information about the medals created by a corporation."""
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

    @api.auto_call('corp/MemberMedals')
    def member_medals(self, api_result=None):
        """Returns information about medals assigned to corporation members."""
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

    @api.auto_call('corp/ContainerLog')
    def container_log(self, api_result=None):
        """Returns a log of actions performed on corporation containers."""
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

    @api.auto_call('corp/Locations', map_params={'location_list': 'IDs'})
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

    @api.auto_call('corp/Blueprints')
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

    @api.auto_call('corp/Facilities')
    def facilities(self, api_result=None):
        rowset = api_result.result.find('rowset')
        rows = rowset.findall('row')

        results = {}
        for row in rows:
            a = row.attrib
            results[int(a['facilityID'])] = {
                'region': {
                    'id': int(a['regionID']),
                    'name': a['regionName'],
                },
                'system': {
                    'id': int(a['solarSystemID']),
                    'name': a['solarSystemName'],
                },
                'starbase_modifier': float(a['starbaseModifier']),
                'tax': float(a['tax']),
                'type_id': int(a['typeID']),
                'type_name': a['typeName'],
            }
        return api.APIResult(results, api_result.timestamp, api_result.expires)

    @api.auto_call('corp/CustomsOffices')
    def customs_offices(self, api_result=None):
        rowset = api_result.result.find('rowset')
        rows = rowset.findall('row')

        results = {}
        for row in rows:
            a = row.attrib
            results[int(a['itemID'])] = {
                'system': {
                    'id': int(a['solarSystemID']),
                    'name': a['solarSystemName'],
                },
                'permissions': {
                    'alliance': a['allowAlliance'] == 'True',
                    'standings': a['allowStandings'] == 'True',
                    'minimum_standing': float(a['standingLevel']),
                },
                'reinforce_hour': int(a['reinforceHour']),
                'tax_rate': {
                    'alliance': float(a['taxRateAlliance']),
                    'corp': float(a['taxRateCorp']),
                    'standings': {
                        'high': float(a['taxRateStandingHigh']),
                        'good': float(a['taxRateStandingGood']),
                        'neutral': float(a['taxRateStandingNeutral']),
                        'bad': float(a['taxRateStandingBad']),
                        'horrible': float(a['taxRateStandingHorrible']),
                    },
                },
            }
        return api.APIResult(results, api_result.timestamp, api_result.expires)


# vim: set ts=4 sts=4 sw=4 et:
