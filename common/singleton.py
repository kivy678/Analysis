# -*- coding:utf-8 -*-

class Singleton:
    _instance = None

    @classmethod
    def _getInstance(cls):
        return cls._instance

    @classmethod
    def instance(cls, *args, **kargs):

        cls._instance = cls(*args, **kargs)
        cls.instance = cls._getInstance
        return cls._instance
