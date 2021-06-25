#!/usr/bin/env python
# -*- coding=UTF-8 -*-

from lib.east_web import east_web
from lib.BaseModel import BaseModel
import time
from config import Config
import sys
import datetime
from chinese_calendar import is_workday, is_holiday


class modify(object):

    def __init__(self):
        self.Config = Config()
        self.Model = BaseModel(self.Config.mysql)
        self.east = east_web()
        self._t = round(time.time() * 1000)

    def clear_code(self):
        r = self.Model.update_One('update stock set weight = 0')
        print(r)

    def code(self, code_str):
        for item in list(row.split(":") for row in code_str.split("/")):
            code = item[0]
            try:
                weight = item[1]
            except:
                weight = 10
            r = self.Model.update_One("update stock set weight = '{}' where code='{}'".format(weight,code))
            print(r)

    def clear_bk(self):
        r = self.Model.update_One('update bk set weight = 0')
        print(r)

    def bk(self, bk_str):
        for item in list(row.split(":") for row in bk_str.split("/")):
            bk_code = item[0]
            try:
                weight = item[1]
            except:
                weight = -1
            r = self.Model.update_One("update bk set weight = '{}' where bk_code='{}'".format(weight,bk_code))
            print(r)


def init():
    return modify()

if __name__ == '__main__':
    obj = modify()