# Notes
Fork this repository before the work and open a pull request after so we can see you finished. Both assignments must be done in Python 3 with the use of any packages you see fit. When assessing the results, we'll pay special attention to performance of your code, so try to make it optimized.

# Test Assignment No. 1
1. Get [a list](https://raw.githubusercontent.com/dwyl/english-words/master/words.txt) of English words.
2. Select 100 random entries that satisfy these conditions:
   * They begin with a lowercase letter.
   * They only contain letters.
3. Search those entries on [DuckDuckGo](https://duckduckgo.com).
4. Save the titles of top three results.


**Expected outcome**: a JSON of the following structure:
```
{"flower": ["title 1", "title 2", "title 3"], "cow": ["title 1", "title 2", "title 3], ...}
```

# Usage


```python
    >>> from test-assignment import DictService
    >>>
    >>> search = DictService()
    >>> # search multiple words
    >>> results = search_engine.search_duck_duck_go(['France', 'Russia'])
    >>> results
    ... [{...}, {...}]
    >>> # search single word
    >>> results = search_engine.search_duck_duck_go(['Ireland'])
    >>> # top 3 results
    >>> DictService.get_top_3(results[0])
    ... ['Ireland An island in the North Atlantic.',
    ...  'Northern Ireland A part of the United Kingdom in the ',
    ...  'United Kingdom of Great Britain and Ireland A sovereign']
    ...
    >>> search.get_word()  # Get one random word given url
    ... 'transportingly'
    >>>
    >>> search.s.list_all_words()  # List 100 random words
    ... ['eradicatory', 'becomingness','sidetracking', ....]
    >>>
    >>> len(search.list_all_words())
    ... 100
    >>>  search.search_all()  # Search 100 random words from file on DuckDuckGo and save to file.
    >>>
```

# Test Assignment No. 2
Turn the script you created earlier into a proxy service. It should response to `GET` requests at `/search/duckduckgo/{search term}` and return JSON arrays of up to three titles of the top results. Queries must be cached, so if a term is looked up twice, first it will be a request to DuckDuckGo and second will be a result from the cache. Write unit tests for your code with the use of `unittest` and `unittest.mock` modules.


# Usage
To start the app please note that the dev server will not work fine with this setup due to the event loop


```bash
    cd test-assignment
    gunicorn --bind 0.0.0.0:8000 wsgi
```

Looking up a query for the first time will hit DuckDuckGo and you will see `cached = false`

```bash
    curl http://127.0.0.1:8000/search/duckduckgo/google/
    {
      "cached": false,
      "google": [
        "Google An American multinational technology company that specializes in Internet-related services...",
        "Google Search A web search engine developed by Google.",
        "Goggles Goggles, or safety glasses, are forms of protective eyewear that usually enclose or protect the..."
      ]
    }
```

Looking up a query for the 2nd time will not hit DuckDuckGo and you will see `cached = true`


```bash
curl http://127.0.0.1:8000/search/duckduckgo/google/
{
  "cached": true,
  "google": [
    "Google An American multinational technology company that specializes in Internet-related services...",
    "Google Search A web search engine developed by Google.",
    "Goggles Goggles, or safety glasses, are forms of protective eyewear that usually enclose or protect the..."
  ]
}
```


Looking up a query that may be cached but you don't want a cached version


```bash
curl http://127.0.0.1:8000/search/duckduckgo/google?use-cache=false
{
  "cached": false,
  "google": [
    "Google An American multinational technology company that specializes in Internet-related services...",
    "Google Search A web search engine developed by Google.",
    "Goggles Goggles, or safety glasses, are forms of protective eyewear that usually enclose or protect the..."
  ]
}
```


**Expected outcome**: a publicly availble web service.
