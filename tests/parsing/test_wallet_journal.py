import unittest2 as unittest

from tests.utils import make_api_result

from evelink.parsing import wallet_journal as evelink_w

class WalletJournalTestCase(unittest.TestCase):
    def test_wallet_journal(self):
        api_result = make_api_result("char/wallet_journal.xml")

        result = evelink_w.parse_wallet_journal(api_result)

        self.assertEqual(result, [{
            'amount': -10000.0,
            'arg': {'id': 0, 'name': '35402941'},
            'balance': 985620165.53,
            'timestamp': 1291962600,
            'id': 3605301231L,
            'party_1': {'id': 150337897, 'name': 'corpslave12'},
            'party_2': {'id': 1000132, 'name': 'Secure Commerce Commission'},
            'reason': '',
            'tax': {'amount': 0.0, 'taxer_id': 0},
            'type_id': 72},
        {
            'amount': -10000.0,
            'arg': {'id': 0, 'name': '35402950'},
            'balance': 985610165.53,
            'timestamp': 1291962600,
            'id': 3605302609L,
            'party_1': {'id': 150337897, 'name': 'corpslave12'},
            'party_2': {'id': 1000132, 'name': 'Secure Commerce Commission'},
            'reason': '',
            'tax': {'amount': 0.0, 'taxer_id': 0},
            'type_id': 72},
        {
            'amount': -10000.0,
            'arg': {'id': 0, 'name': '35402956'},
            'balance': 985600165.53,
            'timestamp': 1291962660,
            'id': 3605303380L,
            'party_1': {'id': 150337897, 'name': 'corpslave12'},
            'party_2': {'id': 1000132, 'name': 'Secure Commerce Commission'},
            'reason': '',
            'tax': {'amount': 0.0, 'taxer_id': 0},
            'type_id': 72},
        {
            'amount': -10000.0,
            'arg': {'id': 0, 'name': '35402974'},
            'balance': 985590165.53,
            'timestamp': 1291962720,
            'id': 3605305292L,
            'party_1': {'id': 150337897, 'name': 'corpslave12'},
            'party_2': {'id': 1000132, 'name': 'Secure Commerce Commission'},
            'reason': '',
            'tax': {'amount': 0.0, 'taxer_id': 0},
            'type_id': 72},
        {
            'amount': -10000.0,
            'arg': {'id': 0, 'name': '35402980'},
            'balance': 985580165.53,
            'timestamp': 1291962720,
            'id': 3605306236L,
            'party_1': {'id': 150337897, 'name': 'corpslave12'},
            'party_2': {'id': 1000132, 'name': 'Secure Commerce Commission'},
            'reason': '',
            'tax': {'amount': 0.0, 'taxer_id': 0},
            'type_id': 72},
        ])
