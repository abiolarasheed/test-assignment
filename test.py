# -*- coding: utf-8 -*-
"""
    test-assignment.test
    ~~~~~~~~~

    This script exposes the main search.

    :copyright: © 2018 by the Abiola Rasheed.
    :license: PRIVATE PROPERTY.
"""
import json
from unittest import mock, TestCase

from models import DictService
from views import application as app


response_json = [{'yelp': ["Yelf's Hotel, Ryde - Best Price Guarantee.",
                           'Restaurants, Dentists, Bars, Beauty Salons, Doctors - Yelp',
                           'Yelp - Wikipedia']}
                 ]


# Fake redis storage
cache = {}


class MockRedis:
    @staticmethod
    def get(words):
        return cache.get(words)

    @staticmethod
    def set(key, value):
        global cache

        return cache.update({key: value})


def mock_search(words):
    class MockDictService(DictService):
        def search_duck_duck_go(self, searched_term):
            return response_json
    return MockDictService()


@mock.patch.object(DictService, 'search_duck_duck_go', return_value=response_json)
class DictServiceTestCase(TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_search(self, word):
        with mock.patch('views.cache.get', side_effect=MockRedis.get):
            with mock.patch('views.cache.set', side_effect=MockRedis.set):
                result = self.app.get('/search/duckduckgo/yelp')

                # assert the status code of the response
                self.assertEqual(result.status_code, 200)

                # convert response json to dict
                data = json.loads(result.data)

                # Test key work in response
                self.assertIn('yelp', data.keys())

                # Test the response content
                self.assertListEqual(sorted(data['yelp']), sorted(response_json[0]["yelp"]))

                # Test response was not from cache on 1st request
                self.assertEqual(data.get("cached"), False)

                # Test cache on second call to same url
                result = self.app.get('/search/duckduckgo/yelp')
                # convert response json to dict
                data = json.loads(result.data)

                # Test that result on 2nd call was from cache
                self.assertEqual(data.get("cached"), True)

                # Test disable cache via query string works
                result = self.app.get('/search/duckduckgo/yelp?use-cache=false')
                # convert response json to dict
                data = json.loads(result.data)
                self.assertEqual(data.get("cached"), False)
