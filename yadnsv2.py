#!/usr/bin/python3
__author__ = 'deface'

import requests
import json
import logging
import re
import sys

class YandexDNS:
    # API URLS
    host = "https://pddimp.yandex.ru/api2/admin/dns/"
    request = ""
    response = ""
    records = []


    def __init__(self, domain, token):
        self.domain = domain
        self.token = token
        logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG,
                            filename='dns_updater.log')
        self._get_records()

    def _send(self, url, data=None):
        if data is not None:
            data = parse.urlencode(data).encode("utf-8")
        resp = requests.get(self.host + url, data=data, headers={'PddToken': self.token})
        return json.loads(resp.content.decode('utf-8'))

    def update(self, data, query=None, custom=None):
        if custom is not None and len(custom):
            records = custom
        else:
            records = self.records
        if query is not None:
            records = self._query(query)

        for rec in records:
            for key in data.keys():
                rec[key] = data[key]
            logging.info("Updating " + rec[key])
            self._send("edit", rec)

    def list(self, query=None):
        if query is not None:
            return self._query(query)
        return self.records

    def _get_records(self):
        response = self._send("list?domain=" + self.domain)
        self.records = response['records']

    def _query(self, query):
        result = []
        match = True
        return query

    def add(self, record):
        if "type" not in record.keys() or "content" not in record.keys():
            raise Exception("type or content not found in record")
        self._send("add", record)

    def delete(self):
        pass

if __name__ == '__main__':
    yad = YandexDNS(domain=sys.argv[1], token=sys.argv[2])

    print ('\n'.join(['{subdomain} {type} {content} {ttl}'.format(**d) for d in yad.list()]))

