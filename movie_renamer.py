#!/usr/bin/env python

import glob
import re
import os
import time
import omdb
from titlecase import titlecase

MOVIE_DIR = '/movies'
pass_same_check = 0

def clean_filename(filename):
    filename = titlecase(filename)
    filename = re.sub('(720p|1080p|DVDRip|R5|MULTi|BluRay|REPACK|BDRip|PROPER).*', '', filename)
    filename = re.sub('\.', ' ', filename)
    filename = re.sub('\_', ' ', filename)
    filename = re.sub('Iii', 'III', filename)
    filename = re.sub('Ii', 'II', filename)
    filename = re.sub(' v ', ' V ', filename)
    filename = re.sub('\s+', ' ', filename).strip()
    return filename

dirs = sorted(glob.glob(MOVIE_DIR + '/*'))
for item in dirs:
    m = re.search('([0-9\_\-a-zA-Z\s\'\.]+)(\s|_|\.)(|\()(19[0-9]{2}|20[0-9]{2})(\)|)', item)
    pass_same_check = 0
    date = None

    # found title and date
    if m and m.group(1) and m.group(4):
        filename = m.group(1)
        date = m.group(4)

    # Found only title
    elif m and m.group(1):
        filename = m.group(1).rstrip()
        old_filename = m.group(0)
    elif m:
        filename = m.group(0).rstrip()
        old_filename = m.group(0)
    else:
        filename = os.path.basename(item)
        pass_same_check = 1

    # Clean up filename
    new_filename = clean_filename(filename)

    # Look up date from omdb
    if date is None:
        date = omdb.get_movie_date(filename)

    if date:
        new_filename = '%s (%s)' % (new_filename, date)

    if new_filename is filename:
        print 'no need to rename file: ' + new_filename + " == " + filename
        continue

    # print '[%s] [%s]' % (new_filename, filename)
    new_path = MOVIE_DIR + '/' + new_filename

    if os.path.exists(new_path):
        print 'ERROR: file already exists: ' + new_path
        continue

    #print '[%s] [%s]' % (new_filename, filename)
    print new_filename
    input = raw_input('Rename?(y/n): ')
    if input == 'y':
        print 'MOVE: ' + item + ' TO ' + new_path
        os.rename(item, new_path)
    elif input == 'exit':
        exit()
