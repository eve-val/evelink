import mock

import evelink.char as evelink_char
from tests.utils import APITestCase

class CharTestCase(APITestCase):

    def setUp(self):
        super(CharTestCase, self).setUp()
        self.char = evelink_char.Char(api=self.api)

    def test_wallet_info(self):
        self.api.get.return_value = self.make_api_result(r"""
          <result>
            <rowset name="accounts" key="accountID" columns="accountID,accountKey,balance">
              <row accountID="1" accountKey="1000" balance="209127923.31" />
            </rowset>
          </result>
        """)

        result = self.char.wallet_info(1)

        self.assertEqual(result, 
            { 
                'balance': 209127923.31,
                'id': 1,
                'key': 1000,
            }
        )
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/AccountBalance', {'characterID': 1}),
            ])

    def test_wallet_balance(self):
        self.api.get.return_value = self.make_api_result(r"""
          <result>
            <rowset name="accounts" key="accountID" columns="accountID,accountKey,balance">
              <row accountID="1" accountKey="1000" balance="209127923.31" />
            </rowset>
          </result>
        """)

        result = self.char.wallet_balance(1)

        self.assertEqual(result, 209127923.31)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/AccountBalance', {'characterID': 1}),
            ])

    def test_industry_jobs(self):
        self.api.get.return_value = self.make_api_result(r"""
            <result>
                <rowset name="jobs" key="jobID">
                    <row jobID="37051255" assemblyLineID="101335750"
                        containerID="61000211" installedItemID="664432163"
                        installedItemLocationID="61000211"
                        installedItemQuantity="1"
                        installedItemProductivityLevel="11"
                        installedItemMaterialLevel="90"
                        installedItemLicensedProductionRunsRemaining="-1"
                        outputLocationID="61000211" installerID="975676271"
                        runs="75" licensedProductionRuns="0"
                        installedInSolarSystemID="30001233"
                        containerLocationID="30001233" materialMultiplier="1"
                        charMaterialMultiplier="1.25"
                        timeMultiplier="0.699999988079071"
                        charTimeMultiplier="0.800000011920929"
                        installedItemTypeID="894" outputTypeID="193"
                        containerTypeID="21644" installedItemCopy="0" completed="0"
                        completedSuccessfully="0" installedItemFlag="4"
                        outputFlag="4" activityID="1" completedStatus="0"
                        installTime="2009-02-01 15:07:00"
                        beginProductionTime="2009-02-01 15:07:00"
                        endProductionTime="2009-02-01 17:59:00"
                        pauseProductionTime="0001-01-01 00:00:00" />
                    <row jobID="19962573" assemblyLineID="100502936"
                        containerID="61000139" installedItemID="178470781"
                        installedItemLocationID="61000139"
                        installedItemQuantity="1"
                        installedItemProductivityLevel="0"
                        installedItemMaterialLevel="0"
                        installedItemLicensedProductionRunsRemaining="-1"
                        outputLocationID="61000139" installerID="975676271"
                        runs="20" licensedProductionRuns="0"
                        installedInSolarSystemID="30002903"
                        containerLocationID="30002903" materialMultiplier="1"
                        charMaterialMultiplier="1.25" timeMultiplier="1"
                        charTimeMultiplier="0.949999988079071"
                        installedItemTypeID="27309" outputTypeID="27309"
                        containerTypeID="21644" installedItemCopy="0" completed="0"
                        completedSuccessfully="0" installedItemFlag="4"
                        outputFlag="0" activityID="4" completedStatus="0"
                        installTime="2008-03-13 15:50:00"
                        beginProductionTime="2008-03-17 22:35:00"
                        endProductionTime="2008-04-13 07:55:00"
                        pauseProductionTime="0001-01-01 00:00:00" />
                </rowset>
            </result>

        """)

        result = self.char.industry_jobs(1)

        self.assertEqual(result, { 
            19962573: {
                'activity_id': 4,                                                                                                 'begin_ts': 1205793300,
                'delivered': False,
                'status': 'failed',
                'finished': False,
                'container_id': 61000139,
                'container_type_id': 21644,
                'end_ts': 1208073300,
                'input': {
                    'id': 178470781,
                    'is_bpc': False,
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
                    'is_bpc': False,
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
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/IndustryJobs', {'characterID': 1}),
            ])
