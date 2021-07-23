#!/usr/bin/env python
# -*- coding=UTF-8 -*-

from lib.east_web import east_web
from lib.BaseModel import BaseModel
import time
from config import Config
import sys
import datetime
from chinese_calendar import is_workday, is_holiday

class bk(object):

    def __init__(self):
        self.Config = Config()
        self.Model = BaseModel(self.Config.mysql)
        self.east = east_web()
        self._t = round(time.time() * 1000)

    def save_bk(self):
        updated = datetime.date.today()

        if is_workday(updated) == False:
            print('Error:{} not work...'.format(updated))
            return

        page = 1
        limit = 100
        while True:
            print(page)
            try:
                result = self.east.get_bk(page,limit,'',False)
            except TypeError as e:
                print(repr(e))
                print('over')
                sys.exit()
            except Exception as e:
                break
            for row in result:

                bk_id = int(row['f12'][2:])

                sql = """INSERT INTO bk (id,bk_name,bk_code,rate,rate_3) VALUE('{}','{}','{}','{}','{}') ON DUPLICATE KEY UPDATE 
                    id = VALUES( id ),
                    bk_name = VALUES( bk_name ),
                    bk_code = VALUES( bk_code ),
                    rate = VALUES( rate ),
                    rate_3 = VALUES( rate_3 )
                """.format(bk_id, row['f14'], row['f12'], row['f3'],row['f127'])
                self.Model.update_One(sql)

            page = page + 1



def init():
    return bk()

if __name__ == '__main__':
    obj = bk()