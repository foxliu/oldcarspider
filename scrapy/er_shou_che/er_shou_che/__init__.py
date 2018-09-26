# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
import scrapy
import requests


engine = sqlalchemy.create_engine(
    scrapy.utils.project.get_project_settings().get('SQLALCHEMY_DATABASE_URI'), echo=False)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

def get_city():
    r = requests.get(
        scrapy.utils.project.get_project_settings().get('CITY_NAME_URL'))
    r.encoding = 'gb2312'
    result = dict()
    if r.status_code == 200:
        city_json = r.json()
        for prov in city_json.get('provinces'):
            prov_name = prov.get('provinceName')
            for city in prov.get('citys'):
                city_name = city.get('citysName').replace(u'市', '')
                c_p = result.get(city_name, None)
                if c_p:
                    result[city_name] = c_p + " " + prov_name
                else:
                    result[city_name] = prov_name
    return result


citys = get_city()
