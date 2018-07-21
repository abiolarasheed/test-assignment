#!/usr/bin/env python3

WORDS_FILE_NAME = 'words.txt'


def get_words(words_file_name):
    words = set()  # skip duplicates
    with open(words_file_name) as words_file:
        for line in words_file:
            # skip a line if it starts or ends with whitespace
            stripped_line = line.strip('\n')
            if stripped_line[0].islower() and stripped_line.isalpha():
                words.add(stripped_line)
    return words


if __name__ == "__main__":
    print(len(get_words(WORDS_FILE_NAME)))
