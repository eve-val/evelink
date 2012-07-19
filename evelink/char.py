from evelink import api
from evelink import constants

class Char(object):
    """Wrapper around /char/ of the EVE API.

    Note that a valid API key is required.
    """

    def __init__(self, api):
        self.api = api

    def wallet_info(self, character_id):
        """Return a given character's wallet."""
        api_result = self.api.get('char/AccountBalance',
            {'characterID': character_id})

        rowset = api_result.find('rowset')
        row = rowset.find('row')
        result = { 
            'balance': float(row.attrib['balance']),
            'id': int(row.attrib['accountID']),
            'key': int(row.attrib['accountKey']),
        }
        return result

    def wallet_balance(self, character_id):
        """Helper to return just the balance from a given character wallet"""

        return self.wallet_info(character_id)['balance']

    def industry_jobs(self, character_id):
        """Get a list of jobs for a character"""

        api_result = self.api.get('char/IndustryJobs',
            {'characterID': character_id})

        rowset = api_result.find('rowset')
        result = {}

        if rowset is None:
            return

        for row in rowset.findall('row'):
            # shortcut to make the following block less painful
            a = row.attrib
            jobID = int(a['jobID'])
            result[jobID] = {
                'line_id': int(a['assemblyLineID']),
                'container_id': int(a['containerID']),
                'input': {
                    'id': int(a['installedItemID']),
                    'is_bpc': a['installedItemCopy'] == '1',
                    'location_id': int(a['installedItemLocationID']),
                    'quantity': int(a['installedItemQuantity']),
                    'prod_level': int(a['installedItemProductivityLevel']),
                    'mat_level': int(a['installedItemMaterialLevel']),
                    'runs_left': int(a['installedItemLicensedProductionRunsRemaining']),
                    'item_flag': int(a['installedItemFlag']),
                    'type_id': int(a['installedItemTypeID']),
                },
                'output': {
                    'location_id': int(a['outputLocationID']),
                    'bpc_runs': int(a['licensedProductionRuns']),
                    'container_location_id': int(a['containerLocationID']),
                    'type_id': int(a['outputTypeID']),
                    'flag': int(a['outputFlag']),
                },
                'runs': int(a['runs']),
                'installer_id': int(a['installerID']),
                'system_id': int(a['installedInSolarSystemID']),
                'multipliers': {
                    'material': float(a['materialMultiplier']),
                    'char_material': float(a['charMaterialMultiplier']),
                    'time': float(a['timeMultiplier']),
                    'char_time': float(a['charTimeMultiplier']),
                },
                'container_type_id': int(a['containerTypeID']),
                'delivered': a['completed'] == '1',
                'finished': a['completedSuccessfully'] == '1',
                'status': constants.Industry.job_status[int(a['completedStatus'])],
                'activity_id': int(a['activityID']),
                'install_ts': api.parse_ts(a['installTime']),
                'begin_ts': api.parse_ts(a['beginProductionTime']),
                'end_ts': api.parse_ts(a['endProductionTime']),
                'pause_ts': api.parse_ts(a['pauseProductionTime']),
            }

        return result

    def kills(self, character_id, before_kill=None):
        """Look up recent kills for the given character

        character_id: 
            The ID of the character to look up kills for.
        before_kill:
            Optional. Only show kills before this kill id. (Used for paging.)
        """

        params = {'characterID': character_id}
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
            attackers = row.find("rowset[@name='attackers']")
            for attacker in attackers.findall('row'):
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
            items = row.find("rowset[@name='items']")
            for item in items.findall('row'):
                a = item.attrib
                type_id = int(a['typeID'])
                result[kill_id]['items'][type_id] = {
                    'id': type_id,
                    'flag': int(a['flag']),
                    'dropped': int(a['qtyDropped']),
                    'destroyed': int(a['qtyDestroyed']),
                }
            
        return result
