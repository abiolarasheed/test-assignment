# -*- coding: utf-8 -*-
"""
    test-assignment.views
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


def mock_search(words):
    del words  # Keeps Pycharm happy

    class MockDictService(DictService):
        def search_duck_duck_go(self, searched_term):
            del searched_term
            return response_json
    return MockDictService()


def mock_redis():
    class MockRedis:
        def __init__(self):
            self.cache = {}

        def get(self, words):
            return self.cache.get(words)

        def set(self, key, value):
            return self.cache.update({key: value})

    return MockRedis()


@mock.patch.object(DictService, 'search_duck_duck_go', return_value=response_json)
class DictServiceTestCase(TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_search(self, word):
        del word  # Keeps Pycharm happy
        with mock.patch('views.cache.get', side_effect=mock_redis().get):
            with mock.patch('views.cache.set', side_effect=mock_redis().set):
                result = self.app.get('/search/duckduckgo/yelp')

                # assert the status code of the response
                self.assertEqual(result.status_code, 200)

                # convert response json to dict
                data = json.loads(result.data)
                self.assertIn('yelp', data.keys())

                # convert response json to dict
                data = json.loads(result.data)
                self.assertListEqual(sorted(data['yelp']), sorted(response_json[0]["yelp"]))
