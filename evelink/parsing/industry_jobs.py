from evelink import api
from evelink import constants

def parse_industry_jobs(api_result):
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
                    'blueprint_type': 'copy' if a['installedItemCopy'] == '1' else 'original',
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
