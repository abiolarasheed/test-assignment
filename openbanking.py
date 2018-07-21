#!/usr/bin/env python3

import random

WORDS_FILE_NAME = 'words.txt'
NUM_TO_SEARCH = 100


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
    return sample


if __name__ == "__main__":
    print(len(get_titles(NUM_TO_SEARCH, WORDS_FILE_NAME)))
