# -*- coding:utf-8 -*-

###########################################################################################

import xmltodict
from bs4 import BeautifulSoup

try: import simplejson as json
except ImportError: import json

from util.fsUtils import Join

###########################################################################################

class XmlParser:
    def __init__(self, decomp_path):
        self.decomp_path = decomp_path
        self.res_path    = Join(decomp_path, 'resources')
        self.manifest    = Join(self.res_path, 'AndroidManifest.xml')
        self.strings     = Join(self.res_path, 'res', 'values', 'strings.xml')

    def getPackageName(self):
        try:
            with open(self.manifest, encoding='utf-8') as fr:
                soup = BeautifulSoup(fr, "lxml-xml")
                label = soup.manifest['package']

                return label

        except Exception as e:
            print(e)
            return False

    def getIconName(self):
        try:
            with open(self.manifest, encoding='utf-8') as fr:
                soup = BeautifulSoup(fr, "lxml-xml")
                label = soup.application['android:label'].lstrip('@')

                labelName = label.split('/')[1]

            with open(self.strings, encoding='utf-8') as fr:
                soup = BeautifulSoup(fr, "lxml-xml")
                for elm in soup.find('string', {'name': labelName}):
                    return elm

        except Exception as e:
            print(e)
            return False


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
        return json.dumps(s)

    @staticmethod
    def loads(s):
        return json.loads(s)
