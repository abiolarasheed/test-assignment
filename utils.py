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
import random

from weakref import WeakKeyDictionary

from bs4 import BeautifulSoup


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
                set(sorted_words.append(word))

            # Ensure no duplicate is stored ever
            sorted_words = set(sorted_words)

            # Maintain sorted list only
            sorted_words = sorted(list(sorted_words))
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


async def fetch(session, searched_term, url):
    """Launch requests for an api."""
    delay = random.randint(0, 3)
    await asyncio.sleep(delay)
    async with session.get(url) as response:
        if response.status == 200:
            html_content = await response.read()

            semaphore = asyncio.Semaphore(2)
            # Without this we can't make the statement below wait
            with await semaphore:
                soup = BeautifulSoup(html_content, 'html.parser')
                top_titles = soup.find_all('a', class_='result__a', limit=3)
                results = [title.get_text() for title in top_titles]
                return {searched_term: results}


async def fetch_all(api_list):
    """Launch requests for multiple api."""
    tasks = []
    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        for content in api_list:
            for searched_term, url in content.items():
                task = asyncio.ensure_future(fetch(session, searched_term, url))
                tasks.append(task)  # Create list of tasks
        results = await asyncio.gather(*tasks)  # Gather all the task responses
        return results
