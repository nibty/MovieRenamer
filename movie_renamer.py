#!/usr/bin/env python
# -*- coding: latin-1 -*-

import glob
import regex
import os
import omdb
from titlecase import titlecase
import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logger = logging.getLogger("movie-renamer")

MOVIE_DIR = '/movies'
ALLOW_CASE_INSENSITIVE_WORDS = True
IGNORE_CASE_WORDS = ['of', 'a', 'the', 'and', 'an', 'or', 'nor', 'but', 'is', 'if', 'then', 'else', 'when',
                     'at', 'from', 'by', 'on', 'off', 'for', 'in', 'out', 'over', 'to', 'into', 'with']
SINGLE_LETTER_WORDS = ['i', 'a']

# compares strings but ignores case in some cases
def compare_movie_title(original, new):
    if original == new:
        return True

    if not ALLOW_CASE_INSENSITIVE_WORDS:
        return False

    original_split = original.split()
    new_split = new.split()

    if len(original_split) != len(new_split):
        return False

    i = 0
    for val in original_split:
        if val != new_split[i] and (val.lower() not in IGNORE_CASE_WORDS):
            return False
        i += 1

    return True


# clean movie filenames
def clean_filename(filename):
    filename = titlecase(filename)
    filename = regex.sub('(720p|1080p|DVDRip|R5|MULTi|BluRay|REPACK|BDRip|PROPER|UNRATED|HDTVRiP|LIMITED|OVA|RERiP).*', '', filename)
    filename = regex.sub('\.-\.', ' ', filename)
    filename = regex.sub('-', ' ', filename)
    filename = regex.sub(r'\.(|$\w)', r' \1', filename)
    filename = regex.sub('\_', ' ', filename)
    filename = regex.sub('Iii', 'III', filename)
    filename = regex.sub('Ii', 'II', filename)
    filename = regex.sub(' v ', ' V ', filename)
    filename = regex.sub(", the", ", The", filename)
    filename = regex.sub("\ a \(", " A (", filename)
    filename = regex.sub('\s+', ' ', filename).strip()
    return filename


dirs = sorted(glob.glob(MOVIE_DIR + '/*'))
for item in dirs:
    item = item.decode('utf-8')
    original_filename = os.path.basename(item)
    m = regex.search('([\S \p{L}]+)(\s|_|\.)(|\()(19[0-9]{2}|20[0-9]{2})(\)|)', original_filename)
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
        filename = original_filename

    # Clean up filename
    new_filename = clean_filename(filename)

    # Look up date from omdb
    if date is None:
        logger.info('Getting date for "%s"' % new_filename)
        date = omdb.get_movie_date(new_filename)

    # Append date to clean filename
    if date:
        new_filename = '%s (%s)' % (new_filename, date)

    # Check if rename is needed
    if compare_movie_title(original_filename, new_filename):
        logger.debug('No need to rename: ' + original_filename)
        continue

    # Report possible dupes
    new_path = MOVIE_DIR + '/' + new_filename
    if os.path.exists(new_path):
        logger.warning('Movie already exists. Maybe a Dupe: ' + new_path)
        continue

    # Rename filename
    print 'Rename ' + item + ' TO ' + new_path
    user_input = raw_input('Rename? (y/n): \n')
    if user_input == 'y':
        logger.debug('Renaming ' + item + ' TO ' + new_path)
        os.rename(item, new_path)
    elif user_input == 'exit':
        exit()