import mock
import unittest2 as unittest

import evelink.parsing.industry_jobs as evelink_ij
from tests.utils import make_api_result

class IndustryJobsTestCase(unittest.TestCase):

    def test_parse_industry_jobs(self):
        api_result, _, _ = make_api_result("char/industry_jobs.xml")
        result = evelink_ij.parse_industry_jobs(api_result)
        self.assertEqual(result, {
            19962573: {
                'activity_id': 4,
                'begin_ts': 1205793300,
                'delivered': False,
                'status': 'failed',
                'finished': False,
                'container_id': 61000139,
                'container_type_id': 21644,
                'end_ts': 1208073300,
                'input': {
                    'id': 178470781,
                    'blueprint_type': 'original',
                    'item_flag': 4,
                    'location_id': 61000139,
                    'mat_level': 0,
                    'prod_level': 0,
                    'quantity': 1,
                    'runs_left': -1,
                    'type_id': 27309},
                'install_ts': 1205423400,
                'system_id': 30002903,
                'installer_id': 975676271,
                'line_id': 100502936,
                'multipliers': {
                    'char_material': 1.25,
                    'char_time': 0.949999988079071,
                    'material': 1.0,
                    'time': 1.0},
                'output': {
                    'bpc_runs': 0,
                    'container_location_id': 30002903,
                    'flag': 0,
                    'location_id': 61000139,
                    'type_id': 27309},
                'runs': 20,
                'pause_ts': None},
            37051255: {
                'activity_id': 1,
                'begin_ts': 1233500820,
                'delivered': False,
                'status': 'failed',
                'finished': False,
                'container_id': 61000211,
                'container_type_id': 21644,
                'end_ts': 1233511140,
                'input': {
                    'id': 664432163,
                    'blueprint_type': 'original',
                    'item_flag': 4,
                    'location_id': 61000211,
                    'mat_level': 90,
                    'prod_level': 11,
                    'quantity': 1,
                    'runs_left': -1,
                    'type_id': 894},
                'install_ts': 1233500820,
                'system_id': 30001233,
                'installer_id': 975676271,
                'line_id': 101335750,
                'multipliers': {
                    'char_material': 1.25,
                    'char_time': 0.800000011920929,
                    'material': 1.0,
                    'time': 0.699999988079071},
                'output': {
                    'bpc_runs': 0,
                    'container_location_id': 30001233,
                    'flag': 4,
                    'location_id': 61000211,
                    'type_id': 193},
                'runs': 75,
                'pause_ts': None}
            }
        )
