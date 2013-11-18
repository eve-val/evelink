import mock
import unittest2 as unittest

from tests.utils import make_api_result

from evelink.parsing import wallet_transactions as evelink_w

class TransactionsTestCase(unittest.TestCase):

    def test_parse_wallet_transactions(self):
        api_result, _, _ = make_api_result("char/wallet_transactions.xml")

        result = evelink_w.parse_wallet_transactions(api_result)

        self.assertEqual(result, [
           {'client': {'id': 1034922339, 'name': 'Elthana'},
            'id': 1309776438,
            'action': 'buy',
            'for': 'personal',
            'journal_id': 6256809868L,
            'price': 34101.06,
            'quantity': 1,
            'station': {'id': 60003760,
                        'name': 'Jita IV - Moon 4 - Caldari Navy Assembly Plant'},
            'timestamp': 1265513640,
            'type': {'id': 20495, 'name': 'Information Warfare'}},
           {'client': {'id': 1979235241, 'name': 'Daeja synn'},
            'id': 1307711508,
            'action': 'buy',
            'for': 'personal',
            'journal_id': 6256808968L,
            'price': 1169939.97,
            'quantity': 1,
            'station': {'id': 60015027,
                        'name': 'Uitra VI - Moon 4 - State War Academy School'},
            'timestamp': 1265392020,
            'type': {'id': 11574, 'name': 'Wing Command'}},
           {'client': {'id': 275581519, 'name': 'SPAIDERKA'},
            'char': {'id': 124, 'name': 'Bar'},
            'id': 1304203159,
            'action': 'buy',
            'for': 'personal',
            'journal_id': 6256808878L,
            'price': 13012.01,
            'quantity': 2,
            'station': {'id': 60003760,
                        'name': 'Jita IV - Moon 4 - Caldari Navy Assembly Plant'},
            'timestamp': 1265135280,
            'type': {'id': 3349, 'name': 'Skirmish Warfare'}},
           {'client': {'id': 1703231064, 'name': 'Der Suchende'},
            'char': {'id': 123, 'name': 'Foo'},
            'id': 1298649939,
            'action': 'buy',
            'for': 'personal',
            'journal_id': 6256808869L,
            'price': 556001.01,
            'quantity': 1,
            'station': {'id': 60004369,
                        'name': 'Ohmahailen V - Moon 7 - Corporate Police Force Assembly Plant'},
            'timestamp': 1264779900,
            'type': {'id': 2410, 'name': 'Heavy Missile Launcher II'}}
        ])

