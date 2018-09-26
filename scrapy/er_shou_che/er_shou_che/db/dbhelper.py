# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, DATE, Float
from sqlalchemy import UniqueConstraint
from er_shou_che.db.comm import BaseModel


class CarInfoModel(BaseModel):
    __tablename__ = 'car_info'
    __table_args__ = (UniqueConstraint('url', name='url'),)

    id = Column(Integer, primary_key=True)
    title = Column(String)
    guanzhu = Column(String)
    baomai = Column(String)
    baoyang = Column(String)
    shangpai_time = Column(String)
    licheng = Column(String)
    address = Column(String)
    province = Column(String)
    pailiang = Column(String)
    biansuxiang = Column(String)
    price = Column(Float(asdecimal=True))
    newcarprice = Column(Float(asdecimal=True))
    desc = Column(Text)
    url = Column(String, nullable=False)

