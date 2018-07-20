# -*- coding: utf-8 -*-
"""
    test-assignment.utils
    ~~~~~~~~~

    This script provides utilities for performing various task.

    :copyright: © 2018 by the Abiola Rasheed.
    :license: PRIVATE PROPERTY.
"""

import aiohttp
import asyncio

from weakref import WeakKeyDictionary


class WordDescriptor:
    def __init__(self):
        self.__sorted_words = WeakKeyDictionary()

    def __get__(self, instance, obj_type):
        return self.__sorted_words.get(instance, [])

    def __set__(self, instance, word_or_list):
        sorted_words = self.__sorted_words.get(instance, [])

        if word_or_list:
            if type(word_or_list) is list:
                word_or_list = [self.__class__.word_validator(word) for word in word_or_list]
                sorted_words.extend(word_or_list)

            else:
                word = self.__class__.word_validator(word_or_list)
                sorted_words.append(word)

            self.__sorted_words[instance] = sorted_words

    @staticmethod
    def word_validator(word):
        if word and not isinstance(word, str):
            # Don't allow empty strings or None
            raise TypeError("This input is not a string, enter only string input")

        if not word[0].islower():
            raise TypeError(f"{word} is not a lower case letter")

        if not word.isalpha():
            raise TypeError(f"{word} does not contain only letter")

        return word


async def fetch(session, api):
    """Launch requests for an api."""
    async with session.get(api) as response:
        if response.status == 200:
            return await response.text()


async def fetch_all(api_list):
    """Launch requests for multiple api."""
    tasks = []
    timeout = aiohttp.ClientTimeout(total=20)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        for api in api_list:
            task = asyncio.ensure_future(fetch(session, api))
            tasks.append(task)  # Create list of tasks
        results = await asyncio.gather(*tasks)  # Gather all the task responses
        return results
