# -*- coding: utf-8 -*-

__all__=[
    'CreatePopup'
]

##################################################################################################

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from module.frida.gui.settings import FONT

##################################################################################################

class CreatePopup(Widget):
    def __init__(self, content=''):
        self.popup = BoxLayout(orientation='vertical')
        self.popup.padding = [0, 10, 0, 0]

        self.content = BoxLayout(orientation='vertical')
        self.content.add_widget(Label(text=content, font_name=FONT))
        self.popup.add_widget(self.content)

        self.btn = BoxLayout(orientation='horizontal')
        self.btn.spacing = 6

        self.ok_btn = Button(text='ok')
        self.cancle_btn = Button(text='cancle')

        self.ok_btn.size_hint = (.5, .7)
        self.cancle_btn.size_hint = (.5, .7)

        self.btn.add_widget(self.ok_btn)
        self.btn.add_widget(self.cancle_btn)

        self.popup.add_widget(self.btn)


    def removeButton(self, name):
        if 'cancle' == name:
            self.btn.remove_widget(self.cancle_btn)
            self.ok_btn.size_hint = (0, .60)
            self.btn.padding = [80, 0, 0, 8]

    def default_create(self, obj, name):
        self._popup = Popup(title=name, content=obj, size_hint=(0.9, 0.9))
        self._popup.open()

    def create(self, obj, name):
        self._popup = Popup(content=obj.popup, title=name, size_hint=(None, None), size=(290, 200), auto_dismiss=False)
        obj.ok_btn.bind(on_press=self._popup.dismiss)
        self._popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()


    def setTrigger(self, obj, trg):
        obj.ok_btn.bind(on_press=trg)
