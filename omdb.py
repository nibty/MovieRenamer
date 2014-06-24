import requests
import StringIO
import urllib
import simplejson as json
import re


def get_movie_date(movie_name):
    url = 'http://www.omdbapi.com?t=' + urllib.quote(movie_name)
    r = requests.post(url)
    data = json.loads(r.text)
    date = data.get('Year', None)
    return date
