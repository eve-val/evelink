from evelink import api, constants
from evelink.parsing.assets import parse_assets
from evelink.parsing.contact_list import parse_contact_list
from evelink.parsing.contracts import parse_contracts
from evelink.parsing.industry_jobs import parse_industry_jobs
from evelink.parsing.kills import parse_kills
from evelink.parsing.orders import parse_market_orders
from evelink.parsing.wallet_transactions import parse_wallet_transactions

class Corp(object):
    """Wrapper around /corp/ of the EVE API.

    Note that a valid corp API key is required.
    """

    def __init__(self, api):
        self.api = api

    def industry_jobs(self):
        """Get a list of jobs for a corporation."""

        api_result = self.api.get('corp/IndustryJobs')

        return parse_industry_jobs(api_result)

    def kills(self, before_kill=None):
        """Look up recent kills for a corporation.

        before_kill:
            Optional. Only show kills before this kill id. (Used for paging.)
        """

        params = {}
        if before_kill is not None:
            params['beforeKillID'] = before_kill
        api_result = self.api.get('corp/KillLog', params)

        return parse_kills(api_result)

    def wallet_info(self):
        """Get information about corp wallets."""

        api_result = self.api.get('corp/AccountBalance')

        rowset = api_result.find('rowset')
        results = {}
        for row in rowset.findall('row'):
            wallet = {
                'balance': float(row.attrib['balance']),
                'id': int(row.attrib['accountID']),
                'key': int(row.attrib['accountKey']),
            }
            results[wallet['key']] = wallet

        return results

    def wallet_transactions(self, before_id=None, limit=None):
        """Returns wallet transactions for a corporation."""

        params = {}
        if before_id is not None:
            params['fromID'] = before_id
        if limit is not None:
            params['rowCount'] = limit
        api_result = self.api.get('corp/WalletTransactions', params)

        return parse_wallet_transactions(api_result)

    def orders(self):
        """Return a corporation's buy and sell orders."""
        api_result = self.api.get('corp/MarketOrders')

        return parse_market_orders(api_result)

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
        return parse_assets(api_result)

    def faction_warfare_stats(self):
        """Returns stats from faction warfare if this corp is enrolled.

        NOTE: This will raise an APIError if the corp is not enrolled in
        Faction Warfare.
        """
        api_result = self.api.get('corp/FacWarStats')

        _str, _int, _float, _bool, _ts = api.elem_getters(api_result)

        return {
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

    def contracts(self):
        """Get information about corp contracts."""
        api_result = self.api.get('corp/Contracts')
        return parse_contracts(api_result)

    def shareholders(self):
        """Get information about a corp's shareholders."""
        api_result = self.api.get('corp/Shareholders')

        results = {
            'char': {},
            'corp': {},
        }
        rowsets = dict((r.attrib['name'], r) for r in api_result.findall('rowset'))

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

        return results

    def contacts(self):
        """Return the corp's corp and alliance contact lists."""
        api_result = self.api.get('corp/ContactList')
        return parse_contact_list(api_result)

    def titles(self):
        """Returns information about the corporation's titles."""
        api_result = self.api.get('corp/Titles')

        rowset = api_result.find('rowset')
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

        return results

    def starbases(self):
        """Returns information about the corporation's POSes."""
        api_result = self.api.get('corp/StarbaseList')

        rowset = api_result.find('rowset')
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

        return results

# vim: set ts=4 sts=4 sw=4 et:
