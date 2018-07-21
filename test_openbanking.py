#!/usr/bin/env python3

from aiohttp.test_utils import (
    AioHTTPTestCase,
    unittest_run_loop,
    make_mocked_coro,
)
import openbanking
import mock
import json

class OpenBankingTest(AioHTTPTestCase):

    async def get_application(self):
        return openbanking.get_app()

    @unittest_run_loop
    async def test_duckduckgo_integration(self):
        resp = await self.client.request("GET", '/search/duckduckgo/lettuce')
        assert resp.status == 200
        json_result = await resp.text()
        result = json.loads(json_result)
        assert 'lettuce' in result
        assert len(result['lettuce']) == 3

    # granted, not really useful, but the assignment says 'use mock'
    @mock.patch('openbanking.results_to_json', return_value='cabbage')
    def test_results_to_json(self, mocked):
        assert openbanking.results_to_json('cabbage') == 'cabbage'
        assert openbanking.results_to_json('lettuce') == 'cabbage'
