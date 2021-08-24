# -*- coding:utf-8 -*-

##########################################################################

import os
import uuid

import xml.etree.ElementTree as ET
import xml.etree as etree

##########################################################################

BASE_DIR        = os.path.dirname(os.path.realpath(__file__))
SHARED_DIR      = os.path.join(BASE_DIR, 'shared_prefs')

##########################################################################


class SharedPreferences:
    def __init__(self, fpath):
        self.fpath = fpath
        self.tree = None
        self.root = None

        if not os.path.isfile(fpath):
            self.createXML()

        self.opener()


    def __del__(self):
        del self.tree


    def createXML(self):
        root = ET.Element('map')
        #ET.SubElement(root, 'string', name='').text = ''

        tree = ET.ElementTree(root)
        tree.write(self.fpath)


    def opener(self):
        try:
            self.tree = ET.parse(self.fpath)
            self.root = self.tree.getroot()
            return True

        except Exception as e:
            return False


    def getString(self, key):
        for child in self.root.iter('string'):
            if child.get('name') == key:
                return child.text

        return False


    def getInt(self, key):
        for child in self.root.iter('int'):
            if child.get('name') == key:
                return int(child.text)

        return False


    def getBoolean(self, key):
        for child in self.root.iter('boolean'):
            if child.get('name') == key:
                return True if child.text.lower() == 'true' else False

        return False


    def edit(self):
        return self.Editor(self)



    class Editor:
        def __init__(self, context):
            self.context = context


        def putString(self, key, value):
            if self.hasKey('string', key):
                self.changeElementer('string', key, value)
            else:
                self.insertElementer('string', key, value)


        def putInt(self, key, value):
            if self.hasKey('int', key):
                self.changeElementer('int', key, value)
            else:
                self.insertElementer('int', key, value)


        def putBoolean(self, key, value):
            if self.hasKey('boolean', key):
                self.changeElementer('boolean', key, str(value).lower())
            else:
                self.insertElementer('boolean', key, str(value).lower())


        def hasKey(self, etype, key):
            for child in self.context.root.iter(etype):
                if child.get('name') == key:
                    return True

            return False


        def changeElementer(self, etype, key, value):
            for child in self.context.root.iter(etype):
                if child.get('name') == key:
                    child.text = value


        def insertElementer(self, etype, key, value):
            e = ET.Element(etype, {'name': key})
            e.text = value
            self.context.root.append(e)


        def remove(self, etype, key):
            for child in self.context.root.iter(etype):
                if child.get('name') == key:
                    self.context.root.remove(child)


        def clear(self):
            self.context.root.clear()


        def commit(self):
            path = os.path.join(SHARED_DIR, uuid.uuid4().hex)
            self.context.tree.write(path, encoding='utf-8')

            os.remove(self.context.fpath)
            os.rename(path, self.context.fpath)
