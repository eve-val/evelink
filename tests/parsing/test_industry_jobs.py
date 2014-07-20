import mock

from tests.compat import unittest
from tests.utils import make_api_result

import evelink.parsing.industry_jobs as evelink_ij

class IndustryJobsTestCase(unittest.TestCase):

    def test_parse_industry_jobs(self):
        api_result, _, _ = make_api_result("char/industry_jobs.xml")
        result = evelink_ij.parse_industry_jobs(api_result)
        self.assertEqual(result, {
            229049720: {
                'activity_id': 1,
                'begin_ts': 1405234032,
                'blueprint': {
                    'id': 1012703933072,
                    'location_id': 60002758,
                    'type': {
                        'id': 31599,
                        'name': 'Small Hydraulic Bay Thrusters I Blueprint',
                    },
                },
                'complete_ts': None,
                'completed': False,
                'completor_id': 0,
                'cost': 0.0,
                'duration': 81600,
                'end_ts': 1405315632,
                'facility_id': 60002758,
                'installer': {
                    'id': 93578165,
                    'name': 'Rhals Tea',
                },
                'licensed_runs': 0,
                'pause_ts': None,
                'product': {
                    'location_id': 60002758,
                    'name': 'Small Hydraulic Bay Thrusters I',
                    'probability': 0.0,
                    'type_id': 31598,
                },
                'runs': 68,
                'station_id': 60002758,
                'status': 1,
                'system': {
                    'id': 30002776,
                    'name': 'Annaro',
                },
                'team_id': 0,
            },
            229049806: {
                'activity_id': 1,
                'begin_ts': 1405234119,
                'blueprint': {
                    'id': 1012218751226,
                    'location_id': 60002758,
                    'type': {
                        'id': 31178,
                        'name': 'Small Polycarbon Engine Housing I Blueprint',
                    },
                },
                'complete_ts': None,
                'completed': False,
                'completor_id': 0,
                'cost': 0.0,
                'duration': 81491,
                'end_ts': 1405315610,
                'facility_id': 60002758,
                'installer': {
                    'id': 93578165,
                    'name': 'Rhals Tea',
                },
                'licensed_runs': 0,
                'pause_ts': None,
                'product': {
                    'location_id': 60002758,
                    'name': 'Small Polycarbon Engine Housing I',
                    'probability': 0.0,
                    'type_id': 31177,
                },
                'runs': 83,
                'station_id': 60002758,
                'status': 1,
                'system': {
                    'id': 30002776,
                    'name': 'Annaro',
                },
                'team_id': 0,
            },

        })
