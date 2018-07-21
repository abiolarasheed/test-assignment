#!/usr/bin/env python3

import random
import requests

BASE_URL = 'https://start.duckduckgo.com/html/'
NUM_TO_SEARCH = 5
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


def get_titles(num_to_search, words_file_name):
    words = get_words(words_file_name)
    sample = random.sample(words, num_to_search)
    duck_text = query_duck(sample[0])
    return duck_text


if __name__ == "__main__":
    print(len(get_titles(NUM_TO_SEARCH, WORDS_FILE_NAME)))
