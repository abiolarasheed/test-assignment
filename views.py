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


@application.route('/search/duckduckgo/<searched_term>',
                   methods=['GET'], strict_slashes=False)
def search(searched_term):
    """
    An api for searching duckduckgo.com.
    :param searched_term:
    :return:
    """
    # Here we want to get the value of use-cache (i.e. ?use-cache=true)
    use_cache = request.args.get('use-cache', "true")

    if use_cache.lower() == "false":
        # Disable cache for this request and pull new info from duckduckgo.
        context = {}
    else:
        context = cache.get(searched_term)  # Check the cache 1st

    if context:
        context = json.loads(context)

    else:
        try:
            # Connect to duckduckgo.com make a search and cache the results.
            search_engine = DictService()
            results = search_engine.search_duck_duck_go(searched_term)  # This method returns a list
            context = results[0]  # This method returns a list
        except IndexError:
            pass

        # Don't cache searched_term with no results
        if context:
            context.update({'cached': True})  # This lets user know they are seeing a cached version
            cache.set(searched_term, json.dumps(context))

        # Let user know this is not a cached version
        context.update({'cached': False})
    return jsonify(**context)
