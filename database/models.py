# -*- encoding: utf-8 -*-

################################################################################

from sqlalchemy import Binary, Column, Integer, String, Boolean

from app import db

################################################################################

class DEVICE(db.Model):
    __tablename__ = 'Device'

    id      = Column(Integer, primary_key=True, autoincrement=True)
    model   = Column(String, unique=True)
    cpu     = Column(String)
    sdk     = Column(String)
    su      = Column(Boolean)
    setup   = Column(Boolean)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return "<DEVICE ('%r','%r,'%r,'%r,'%r')>" % (self.model,
                                                        self.cpu,
                                                        self.sdk,
                                                        self.su,
                                                        self.setup)

class APP(db.Model):
    __tablename__ = 'App'

    id      = Column(Integer, primary_key=True, autoincrement=True)
    sha256  = Column(String, unique=True)
    pkg     = Column(String)
    icon    = Column(String)
    ctime   = Column(String)
    parent  = Column(Integer)
    status  = Column(String)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return "<APP ('%r','%r','%r','%r','%r','%r')>" % (self.sha256,
                                                        self.pkg,
                                                        self.icon,
                                                        self.ctime,
                                                        self.parent,
                                                        self.status)
