# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer
from er_shou_che import session
from sqlalchemy.ext.declarative import declarative_base
from er_shou_che import session
import traceback


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    def insert(self):
        session.add(self)
        try:
            session.commit()
        except:
            print traceback.format_exc()
            session.rollback()
