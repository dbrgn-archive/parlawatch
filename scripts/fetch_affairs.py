# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import sys
import json
import logging

import requests


AFFAIRS_URL = 'http://ws.parlament.ch/affairs/'
OUTFILE = 'affairs.json'


def fetch_single(session, affair_id):
    """Fetch a single affair detail."""
    logging.info('Fetching affair {}...'.format(affair_id))
    r = session.get('{}{}'.format(AFFAIRS_URL, affair_id))
    return r.json()


def fetch_collection(session, page=1):
    """Fetch collection of affairs."""
    logging.info('Fetching affair collection page {}...'.format(page))
    r = session.get('{}?pageNumber={}'.format(AFFAIRS_URL, page))
    return r.json()


def fetch_all(start_page=1):
    """Fetch all affairs, write them to an output file as json lines."""
    session = requests.Session()
    session.headers.update({'Accept': 'application/json'})
    outfile = open(OUTFILE, 'a')
    counter = 0
    page_nr = start_page
    while 1:
        page = fetch_collection(session, page_nr)
        for affair in page:
            data = fetch_single(session, affair['id'])
            outfile.write(json.dumps(data) + '\n')
            counter += 1
        last_entry = page[-1]
        if 'hasMorePages' in last_entry and last_entry['hasMorePages'] is True:
            page_nr += 1
        else:
            break
    outfile.close()
    logging.info('Done. Fetched {} affairs.'.format(counter))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    page = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    try:
        fetch_all(start_page=page)
    except:
        import ipdb
        ipdb.set_trace()
