# -*- coding:utf-8 -*-

##################################################################################################

import os

import kivy
from kivy.app import App
from kivy.lang import Builder

kivy.require('1.11.0')                                  # replace with your current kivy version !

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.actionbar import ActionBar

from kivy.properties import ObjectProperty, StringProperty

from module.frida.gui.popup import CreatePopup
from module.frida.gui.context import *
from module.frida.gui.Logger import getLogger

from module.frida.run import FridaRun

from common import getSharedPreferences
from webConfig import PROCESS_PATH, SHARED_PATH

##################################################################################################

kv = os.path.join(os.path.dirname(__file__), 'gui', 'widgets.kv')

with open(kv, encoding='utf-8') as f:
    Builder.load_string(f.read())

sp              = getSharedPreferences(PROCESS_PATH)
PACKAGE_NAME    = sp.getString('pkg')

sp              = getSharedPreferences(SHARED_PATH)
DATA_DIR        = sp.getString('DATA_DIR')

app = None
root = None

##################################################################################################


def getTabBoxID():
    return root.ids.get('CONTEXT_TAB_BOX_ID')


def getContextID(tabName):
    tab_box       = getTabBoxID()
    context_box   = tab_box.ids.get(tabName)
    context       = context_box.ids.get('CONTEXT_ID')

    return context


def trigger(*args):
    with open(os.path.join(DATA_DIR, 'dump.txt'), 'w') as fw:
        context = getContextID('LOG_BOX_ID')
        fw.write(context.text)


class HEADER_BAR(ActionBar):
    def __init__(self, **kwargs):
        super(HEADER_BAR, self).__init__(**kwargs)
        self.fr = None
        self.LOG = None


    def show_load(self):
        pop = CreatePopup()
        content = LoadDialog(cancel=pop.dismiss_popup)
        pop.default_create(content, 'Load File')


    def on_version(self):
        content = f'\n\n      v0.3.0\n\n피드백 안 받습니다.\n    - kivy -'
        pop = CreatePopup(content)
        pop.removeButton('cancle')
        pop.create(pop, 'version')


    def on_save(self):
        content = f'저장합니다.'
        pop = CreatePopup(content)
        pop.removeButton('cancle')
        pop.create(pop, 'Log Save')
        pop.setTrigger(pop, trigger)


    def on_exit(self):
        self.on_stop()
        exit()


    def on_start(self):
        context = getContextID('LOG_BOX_ID')
        context.text = ''

        if not self.LOG:
            self.LOG = getLogger('logLabel.log', context)

        self.fr = FridaRun(PACKAGE_NAME, self.LOG)
        self.fr.attachHook()


    def on_stop(self):
        context = getContextID('LOG_BOX_ID')
        self.fr.dettachHook()


class LoadDialog(BoxLayout):
    cancel = ObjectProperty(None)

    def load_context(self, rpath, filelist):
        if len(filelist) == 0:
            self.cancel()
            return

        tab = getTabBoxID()
        context = getContextID('MODIFY_BOX_ID')
 
        tab.switch_to(tab.tab_list[0])

        with open(os.path.join(filelist[0])) as fr:
            context.text = fr.read()

        self.cancel()


class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

        global root
        root = self


class MainApp(App):
    def build(self):
        global app
        app = App.get_running_app()

        return RootWidget()


def AppRun():
    MainApp().run()


AppRun()
