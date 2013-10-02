# -*- coding: utf-8 -*-
"""fetch_data.py

Fetch data from the parliament REST webservice.

Usage:
    fetch_data.py <resource> [-p <start_page>] [--no-details]

Options:
    -h --help     Show this screen.
    -p            The page to start parsing. Only applies to collections.
    --no-details  Don't fetch detail pages, store data from collections.

"""
from __future__ import print_function, division, absolute_import, unicode_literals

import json
import logging

import requests
from docopt import docopt


BASE_URL = 'http://ws.parlament.ch/'
OUTDIR = ''


class Fetcher(object):

    def __init__(self, resource, start_page, fetch_details):
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/json'})
        self.resource = resource
        self.page = start_page or 1
        self.fetch_details = fetch_details

    def _fetch_single(self, item_id):
        """Fetch a single detail item."""
        logging.info('Fetching {}/{}...'.format(self.resource, item_id))
        url = '{}{}/{}'.format(BASE_URL, self.resource, item_id)
        r = self.session.get(url)
        return r.json()

    def _fetch_collection(self, page=1):
        """Fetch collection."""
        logging.info('Fetching {} collection page {}...'.format(self.resource, page))
        url = '{}{}/?pageNumber={}'.format(BASE_URL, self.resource, page)
        r = self.session.get(url)
        return r.json()

    def fetch_all(self):
        """Fetch all resources, write them to an output file as json lines."""
        outfile = open('{}{}.json'.format(OUTDIR, self.resource.replace('/', '_')), 'a')
        counter = 0
        while 1:
            page = self._fetch_collection(self.page)
            for item in page:
                if self.fetch_details:
                    data = self._fetch_single(item['id'])
                else:
                    data = item
                    if 'hasMorePages' in data:
                        del data['hasMorePages']
                outfile.write(json.dumps(data) + '\n')
                counter += 1
            last_entry = page[-1]
            if 'hasMorePages' in last_entry and last_entry['hasMorePages'] is True:
                self.page += 1
            else:
                break
        outfile.close()
        logging.info('Done. Fetched {} {} items.'.format(counter, self.resource))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    arguments = docopt(__doc__)
    resource = arguments['<resource>']
    start_page = arguments['<start_page>']
    fetch_details = not arguments['--no-details']

    try:
        f = Fetcher(resource, start_page, fetch_details)
        f.fetch_all()
    except Exception as ex:
        import ipdb
        ipdb.set_trace()
