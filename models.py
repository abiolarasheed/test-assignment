# -*- coding: utf-8 -*-
"""
    test-assignment.models
    ~~~~~~~~~

    This script implements the central duck duck go lookup.

    :copyright: © 2018 by the Abiola Rasheed.
    :license: PRIVATE PROPERTY.
"""

import json

import asyncio
import random
import requests

from utils import fetch_all
from utils import WordDescriptor


class DictService:
    """
    A dictionary look up service.
    """
    __sorted_words = WordDescriptor()
    __local_dict = WordDescriptor()

    def __init__(self):
        self.__local_dict = []
        self.__sorted_words = None
        self.word_api = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"
        self.search_api = "https://api.duckduckgo.com/"

    def load_words(self):
        """
        Return all the word in our url
        :return: list
        """
        # Check local cache and return if exist
        if self.__local_dict:
            return self.__local_dict

        # Connect to internet and get words then cache for reuse
        res = requests.get(self.word_api)
        res_list = res.content.decode("utf-8").splitlines()

        self.__local_dict = [word for word in res_list if word[0] and word[0].islower() and word.isalpha()]
        return self.__local_dict

    def get_word(self):
        """
        Return a single word from our url
        :return: str
        """
        not_found = True
        rand_word = None
        words = self.load_words()

        while not_found:
            rand_word = random.choice(words)
            if rand_word not in self.__sorted_words:
                not_found = False

        return rand_word

    def list_all_words(self):
        # Check cache first
        if self.__sorted_words:
            return self.__sorted_words

        # Search from internet/local store then cache
        self.__sorted_words = [self.get_word() for _ in range(100)]
        return self.__sorted_words

    def search_all(self, save=False):
        """
        Search for all 100 words
        :return:
        """
        words = self.list_all_words()
        results = self.search_duck_duck_go(words)

        if save:
            self.save_to_file(results)

        return results

    def create_api(self, word):
        """
        Create the the api endpoint
        :param word:
        :return:
        """
        return f"{self.search_api}?q={word}&format=json&pretty=1"

    def search_duck_duck_go(self, words):
        """
        Makes an api call to Duck Duck Go
        :param words: String or List to Strings we want to search for.
        :return:
        """
        if type(words) != list:
            words = [words]

        api_list = [self.create_api(word) for word in words]

        loop = asyncio.get_event_loop()  # event loop
        future = asyncio.ensure_future(fetch_all(api_list))  # tasks to do
        results = loop.run_until_complete(future)  # loop until done
        return [result for result in filter(None, results)]

    @staticmethod
    def get_top_3(json_text):
        """
        Return the top 3 results
        :param json_text:
        :return:
        """
        if type(json_text) is dict:
            results = json_text["RelatedTopics"]

        else:
            results = json.loads(json_text, encoding='utf-8')["RelatedTopics"]
        if results:
            results = results[:3]
            new_results = []
            for result in results:
                try:
                    result = result['Text']
                except KeyError:
                    result = result['Topics'][0]['Text']
                finally:
                    new_results.append(result)
            return new_results

        return results

    def save_to_file(self, data_list):
        """
        Save data to json file
        :return:
        """
        cleaned_data = {}

        for data in data_list:
            data = json.loads(data)

            if data['Heading']:
                cleaned_data.update({data['Heading'].lower(): self.__class__.get_top_3(data)})

        with open('data.json', 'w', encoding='utf-8') as outfile:
            json.dump(cleaned_data, outfile, indent=4, ensure_ascii=False)
