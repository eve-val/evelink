import mock
import unittest2 as unittest

import evelink.corp as evelink_corp
from tests.utils import APITestCase

class CorpTestCase(APITestCase):

    def setUp(self):
        super(CorpTestCase, self).setUp()
        self.corp = evelink_corp.Corp(api=self.api)

    @mock.patch('evelink.corp.parse_industry_jobs')
    def test_industry_jobs(self, mock_parse):
        self.api.get.return_value = mock.sentinel.industry_jobs_api_result
        mock_parse.return_value = mock.sentinel.industry_jobs

        result = self.corp.industry_jobs()

        self.assertEqual(result, mock.sentinel.industry_jobs)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/IndustryJobs'),
            ]) 
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.industry_jobs_api_result),
            ])


if __name__ == "__main__":
    unittest.main()
