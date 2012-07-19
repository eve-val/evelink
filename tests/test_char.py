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

    def test_kills(self):
        self.api.get.return_value = self.make_api_result(r"""
          <result> 
              <rowset name="kills" key="killID">
                  <row killID="15640551" solarSystemID="30001160" killTime="2010-11-24 15:29:00" moonID="0">
                      <victim characterID="150080271" characterName="Pilot 333"
                          corporationID="1254875843" corporationName="Starbase Anchoring Corp"
                          allianceID="1254074" allianceName="EVE Gurus"
                          factionID="0" factionName="" damageTaken="446"
                          shipTypeID="670" />
                      <rowset name="attackers"> 
                          <row characterID="935091361" characterName="ICU123"
                              corporationID="224588600" corporationName="Inkblot Squad"
                              allianceID="5514808" allianceName="Authorities of EVE"
                              factionID="0" factionName=""
                              securityStatus="-0.441287532452161"
                              damageDone="446" finalBlow="1"
                              weaponTypeID="2881" shipTypeID="17932" />
                      </rowset>
                      <rowset name="items" columns="typeID,flag,qtyDropped,qtyDestroyed" />
                  </row>
                  <row killID="15640545" solarSystemID="30001160" killTime="2010-11-24 15:28:00" moonID="0"> 
                      <victim characterID="150080271" characterName="Pilot 333"
                          corporationID="1254875843" corporationName="Starbase Anchoring Corp"
                          allianceID="1254074" allianceName="EVE Gurus"
                          factionID="0" factionName="" damageTaken="446"
                          shipTypeID="670" />
                      <rowset name="attackers"> 
                          <row characterID="935091361" characterName="ICU123"
                              corporationID="224588600" corporationName="Inkblot Squad"
                              allianceID="5514808" allianceName="Authorities of EVE"
                              factionID="0" factionName=""
                              securityStatus="-0.441287532452161"
                              damageDone="446" finalBlow="1"
                              weaponTypeID="2881" shipTypeID="17932" />
                      </rowset>
                      <rowset name="items">
                          <row typeID="5531" flag="0" qtyDropped="1" qtyDestroyed="0" />
                          <row typeID="16273" flag="5" qtyDropped="0" qtyDestroyed="750" />
                          <row typeID="21096" flag="0" qtyDropped="0" qtyDestroyed="1" />
                          <row typeID="2605" flag="0" qtyDropped="0" qtyDestroyed="1" />
                      </rowset>
                  </row>
              </rowset>
          </result>
        """)

        result = self.char.kills(1)

        self.assertEqual(result, {
            15640545: {
                'attackers': {
                    935091361: {
                        'alliance': {
                            'id': 5514808,
                            'name': 'Authorities of EVE'},
                        'corp': {
                            'id': 224588600,
                            'name': 'Inkblot Squad'},
                        'damage': 446,
                        'faction': {
                            'id': 0,
                            'name': ''},
                        'final_blow': True,
                        'id': 935091361,
                        'name': 'ICU123',
                        'sec_status': -0.441287532452161,
                        'ship_type_id': 17932,
                        'weapon_type_id': 2881}},
                'items': {
                    2605: {
                        'destroyed': 1,
                        'dropped': 0,
                        'flag': 0,
                        'id': 2605}, 
                    5531: {
                        'destroyed': 0,
                        'dropped': 1,
                        'flag': 0,
                        'id': 5531}, 
                    16273: {
                        'destroyed': 750,
                        'dropped': 0,
                        'flag': 5,
                        'id': 16273}, 
                    21096: {
                        'destroyed': 1,
                        'dropped': 0,
                        'flag': 0,
                        'id': 21096}}, 
                'id': 15640545, 
                'moon_id': 0,
                'system_id': 30001160,
                'time': 1290612480,
                'victim': {
                    'alliance': {
                        'id': 1254074,
                        'name': 'EVE Gurus'}, 
                    'corp': {
                        'id': 1254875843,
                        'name': 'Starbase Anchoring Corp'},
                    'damage': 446,
                    'faction': {
                        'id': 0,
                        'name': ''},
                    'id': 150080271,
                    'name': 'Pilot 333',
                    'ship_type_id': 670}},
            15640551: {
                'attackers': {
                    935091361: {
                        'alliance': {
                            'id': 5514808,
                            'name': 'Authorities of EVE'},
                        'corp': {
                            'id': 224588600,
                            'name': 'Inkblot Squad'},
                        'damage': 446,
                        'faction': {
                            'id': 0,
                            'name': ''},
                        'final_blow': True,
                        'id': 935091361,
                        'name': 'ICU123',
                        'sec_status': -0.441287532452161,
                        'ship_type_id': 17932,
                        'weapon_type_id': 2881}},
                'items': {},
                'id': 15640551,
                'moon_id': 0,
                'system_id': 30001160,
                'time': 1290612540,
                'victim': {
                    'alliance': {
                        'id': 1254074,
                        'name': 'EVE Gurus'},
                    'corp': {
                        'id': 1254875843,
                        'name': 'Starbase Anchoring Corp'},
                    'damage': 446,
                    'faction': {
                        'id': 0,
                        'name': ''},
                    'id': 150080271,
                    'name': 'Pilot 333',
                    'ship_type_id': 670}}
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/KillLog', {'characterID': 1}),
            ])

    def test_kills_paged(self):
        self.api.get.return_value = self.make_api_result(r"""
          <result> 
              <rowset name="kills" key="killID"/>
          </result>
        """)

        self.char.kills(1, 12345)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/KillLog', {'characterID': 1, 'beforeKillID': 12345}),
            ])

    def test_orders(self):
        self.api.get.return_value = self.make_api_result(r"""
          <result> 
              <rowset name="orders" key="orderID">
                  <row orderID="2579890411" charID="91397530"
                      stationID="60011866" volEntered="2120"
                      volRemaining="2120" minVolume="1" orderState="0"
                      typeID="3689" range="32767" accountKey="1000"
                      duration="90" escrow="0.00" price="5100.00" bid="0"
                      issued="2012-06-26 20:31:52" />
                  <row orderID="2584848036" charID="91397530"
                      stationID="60012550" volEntered="1" volRemaining="1"
                      minVolume="1" orderState="0" typeID="16399" range="32767"
                      accountKey="1000" duration="90" escrow="0.00"
                      price="250000.00" bid="0" issued="2012-07-01 22:51:20" />
              </rowset>
          </result>
        """)

        result = self.char.orders(1)

        self.assertEqual(result, { 
            2579890411L: {
                'account_key': 1000, 
                'char_id': 91397530,
                'duration': 90,
                'amount': 2120,
                'escrow': 0.0,
                'id': 2579890411L,
                'type': 'sell',
                'timestamp': 1340742712,
                'price': 5100.0,
                'range': 32767,
                'amount_left': 2120,
                'status': 'active',
                'station_id': 60011866,
                'type_id': 3689},
            2584848036L: {
                'account_key': 1000,
                'char_id': 91397530,
                'duration': 90,
                'amount': 1,
                'escrow': 0.0,
                'id': 2584848036L,
                'type': 'sell',
                'timestamp': 1341183080,
                'price': 250000.0,
                'range': 32767,
                'amount_left': 1,
                'status': 'active',
                'station_id': 60012550,
                'type_id': 16399}
            })

        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/MarketOrders', {'characterID': 1}),
            ])
