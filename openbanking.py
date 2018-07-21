#!/usr/bin/env python3

import random
import requests
import json
from bs4 import BeautifulSoup  # duckduckgo's api is not full search results

BASE_URL = 'https://start.duckduckgo.com/html/'
NUM_TO_SEARCH = 5
NUM_TOP_TITLES = 3
WORDS_FILE_NAME = 'words.txt'


def query_duck(word):
    payload = {'q': word}
    r = requests.get(BASE_URL, params=payload)
    return r.text


def get_words(words_file_name):
    words = set()  # skip duplicates
    with open(words_file_name) as words_file:
        for line in words_file:
            # skip a line if it starts or ends with whitespace
            stripped_line = line.strip('\n')
            if stripped_line[0].islower() and stripped_line.isalpha():
                words.add(stripped_line)
    return words


def get_titles(num_to_search, num_titles, words_file_name):
    words = get_words(words_file_name)
    sample = random.sample(words, num_to_search)
    results = {}
    for word in sample:
        duck_text = query_duck(word)
        soup = BeautifulSoup(duck_text, 'html.parser')
        titles = soup.find_all('a', class_='result__a', limit=num_titles)
        titles_texts = [title.get_text() for title in titles]
        results[word] = titles_texts
    results_json = json.dumps(results, sort_keys=True, indent=4)
    return results_json


if __name__ == "__main__":
    results = get_titles(NUM_TO_SEARCH, NUM_TOP_TITLES, WORDS_FILE_NAME)
    print(results)
