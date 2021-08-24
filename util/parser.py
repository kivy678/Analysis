# -*- coding:utf-8 -*-

###########################################################################################

import xmltodict
from bs4 import BeautifulSoup

try: import simplejson as json
except ImportError: import json

###########################################################################################

class XmlParser:
    def __init__(self, path):
        self._path = path
        self._soup = None

        self.createParer()

    def createParer(self):
        try:
            with open(self._path) as fr:
                self._soup = BeautifulSoup(fr, "lxml-xml")

                return True

        except Exception as e:
            print(e)
            return False

    def parser(self, tag=None, attr=None):
        for i in self._soup.find_all(tag):
            return i.get(attr)


class JsonParser:
    def __init__(self, path):
        self._path = path

    def parser(self):
        try:
            with open(self._path) as fr:
                return json.dumps(xmltodict.parse(fr.read()),
                                    indent=4,
                                    separators=(',', ': '))

        except Exception as e:
            print(e)
            return False

class JSON:
    @staticmethod
    def dump(s, f):
        json.dump(s, f)

    @staticmethod
    def dumps(s):
        print(s)
        return json.dumps(s)

    @staticmethod
    def loads(s):
        return json.loads(s)
