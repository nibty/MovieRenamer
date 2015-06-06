__author__ = 'nick'

import json
import os

with open('movies.json') as data_file:
    data = json.load(data_file)

for movie in data:
    foldername = "/movies/%s" % movie['release']
    os.mkdir(foldername)