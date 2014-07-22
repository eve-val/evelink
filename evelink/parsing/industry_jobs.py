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
            completed = a['completedCharacterID'] != '0'
            result[jobID] = {
                'activity_id': int(a['activityID']),
                'blueprint': {
                    'id': int(a['blueprintID']),
                    'location_id': int(a['blueprintLocationID']),
                    'type': {
                        'id': int(a['blueprintTypeID']),
                        'name': a['blueprintTypeName'],
                    },
                },
                'completed': completed,
                'complete_ts': api.parse_ts(a['completedDate']),
                'completor_id': int(a['completedCharacterID']),
                'cost': float(a['cost']),
                'end_ts': api.parse_ts(a['endDate']),
                'facility_id': int(a['facilityID']),
                'installer': {
                    'id': int(a['installerID']),
                    'name': a['installerName'],
                },
                'product': {
                    'type_id': int(a['productTypeID']),
                    'location_id': int(a['outputLocationID']),
                    'name': a['productTypeName'],
                    'probability': float(a['probability']),
                },
                'runs': int(a['runs']),
                'licensed_runs': int(a['licensedRuns']),
                'pause_ts': api.parse_ts(a['pauseDate']),
                'system': {
                    'id': int(a['solarSystemID']),
                    'name': a['solarSystemName'],
                },
                'station_id': int(a['stationID']),
                'begin_ts': api.parse_ts(a['startDate']),
                'status': int(a['status']),
                'team_id': int(a['teamID']),
                'duration': int(a['timeInSeconds']),
            }

        return result
