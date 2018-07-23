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
        self.__sorted_words = []
        self.json_file = 'data.json'
        self.word_api = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"
        self.search_api = "https://duckduckgo.com/html/"

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

        # We remove empty words too
        self.__local_dict = [word for word in filter(None, res_list) if word[0].islower() and word.isalpha()]
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
            # return only if this word not already stored
            if rand_word not in self.__sorted_words:
                not_found = False

        return rand_word

    def list_all_words(self):
        # Check cache first
        if self.__sorted_words:
            return self.__sorted_words

        # Search from local storage or internet then cache
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
        return f"{self.search_api}?q={word}"

    def search_duck_duck_go(self, words):
        """
        Makes an api call to Duck Duck Go
        :param words: String or List to Strings we want to search for.
        :return:
        """
        if type(words) != list:
            words = [words]

        # Generate the url to call
        api_list = [{word: self.create_api(word)} for word in words]
        loop = asyncio.get_event_loop()  # event loop
        future = asyncio.ensure_future(fetch_all(api_list))  # tasks to do
        results = loop.run_until_complete(future)  # loop until done
        return results

    def save_to_file(self, data_list):
        """
        Save data to json file
        :return: None
        """
        with open(self.json_file, 'w', encoding='utf-8') as outfile:
            json.dump(data_list, outfile, indent=4, ensure_ascii=False)
            print(f"{self.json_file} saved")
