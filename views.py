# -*- coding: utf-8 -*-
"""
    test-assignment.views
    ~~~~~~~~~

    This script exposes the main search.

    :copyright: © 2018 by the Abiola Rasheed.
    :license: PRIVATE PROPERTY.
"""

import json

from flask import Flask
from flask import jsonify
from flask import request

import redis

from models import DictService

application = Flask(__name__)
application.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

cache = redis.StrictRedis(host="localhost", port=6379,
                          db=0, decode_responses=True)


@application.route('/search/duckduckgo/<search_term>',
                   methods=['GET'], strict_slashes=False)
def search(search_term):
    """
    An api for searching duckduckgo.com.
    :param search_term:
    :return:
    """
    # here we want to get the value of use-cache (i.e. ?use-cache=true)
    use_cache = request.args.get('use-cache', None)

    if use_cache == "false":
        # Disable cache for this request and pull new info from duckduckgo.
        context = None
    else:
        context = cache.get(search_term)  # Check the cache 1st

    if context:
        context = json.loads(context)

    else:
        # Connect to duckduckgo.com make a search and cache the results.
        search_engine = DictService()
        results = search_engine.search_duck_duck_go(search_term)
        results = DictService.get_top_3(results[0])

        context = {search_term: results, 'cached': True}

        # Don't cache search_term with no results
        if results:
            cache.set(search_term, json.dumps(context))

        context.update({'cached': False})

    return jsonify(context)
