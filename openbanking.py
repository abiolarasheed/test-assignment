#!/usr/bin/env python3

import asyncio
from aiohttp import ClientSession, web
import random
import json
from bs4 import BeautifulSoup  # duckduckgo's api is not full search results

BASE_URL = 'https://start.duckduckgo.com/html/?q='

# be careful with the next two variables, duckduckgo bans the ip for 'a few
# hours' if we send more than unspecified number of queries/second
# https://duck.co/help/privacy/ip-blocking
SEMAPHORE_COUNTER = 3  # kinda simultaneous requests
NUM_WORDS_TO_SEARCH = 5

NUM_TOP_TITLES = 3  # how many result titles to return at most
WORDS_FILE_NAME = 'words.txt'

cache = {}  # or lru_cache, pymemoize... will they work with async?


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()


async def bound_fetch(sem, word, session):
    async with sem:
        html = await fetch(f'{BASE_URL}{word}', session)
        soup = BeautifulSoup(html, 'html.parser')
        titles = soup.find_all('a', class_='result__a', limit=NUM_TOP_TITLES)
        titles_texts = [title.get_text() for title in titles]
        return {word: titles_texts}


async def get_results(words):
    """
    Credit: https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html
    """
    tasks = []
    sem = asyncio.Semaphore(SEMAPHORE_COUNTER)
    async with ClientSession() as session:
        for word in words:
            task = asyncio.ensure_future(bound_fetch(sem, word, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        return responses


def get_words(words_file_name):
    words = set()  # skip duplicates
    with open(words_file_name) as words_file:
        for line in words_file:
            # skip a line if it starts or ends with whitespace
            stripped_line = line.strip('\n')
            if stripped_line[0].islower() and stripped_line.isalpha():
                words.add(stripped_line)
    return words


def results_to_json(results):
    combined_results = {}
    for result in results:
        combined_results.update(result)

    results_json = json.dumps(combined_results, sort_keys=True, indent=4)
    return results_json


async def get_titles(sample):
    if sample in cache:
        return cache[sample]
    results = await get_results(sample)

    results_json = results_to_json(results)
    cache[sample] = results_json
    return results_json


async def handle(request):
    word = request.match_info.get('word', 'spam')
    result = await get_titles((word,))
    return web.Response(text=result)


def get_app():
    app = web.Application()
    app.add_routes([web.get('/search/duckduckgo/{word}', handle)])
    return app


if __name__ == "__main__":
    # web app
    app = get_app()
    web.run_app(app)

    # # script
    # words = get_words(WORDS_FILE_NAME)
    # sample = random.sample(words, NUM_WORDS_TO_SEARCH)

    # result = get_titles(sample)
    # print(result)
