#!/usr/bin/env python
# -*- coding=UTF-8 -*-

from lib.dbk_web import dbk_web
from lib.east_web import east_web
from lib.BaseModel import BaseModel
import time
from config import Config
import sys
import datetime
from chinese_calendar import is_workday, is_holiday

class dbk(object):

    def __init__(self):
        self.Config = Config()
        self.Model = BaseModel(self.Config.mysql)
        self.dbk_web = dbk_web()
        self.east_web = east_web()
        self._t = round(time.time() * 1000)

    def help(self):
        data =  (list(filter(lambda m:
                            not m.startswith("__") and
                            not m.endswith("__") and
                            not m.startswith("_") and
                            not m.startswith("dump") and
                            not m.startswith("methods") and
                            callable(getattr(self, m)),dir(self))))
        for row in data:
            if type(row) != list:
                print('|'.join(str(i) for i in data))
                return
            print('|'.join(str(i) for i in row))

    def save(self, table='news_c7f', data={}):
        field_str = '`,`'.join(str(i) for i in data)
        field_val = ','.join('%s' for i in data)
        field_data = list(data[i] for i in data)
        sql = """INSERT IGNORE INTO {}(`{}`)  VALUE({})""".format(table, field_str, field_val)
        return self.Model.update_One(sql, list(str(i) for i in field_data))

    def get_stock_market(self,code):
        if code.startswith('6') or code.startswith('8'):
            return '1' # '沪市'
        elif code.startswith('0') or code.startswith('2') or code.startswith('3'):
            return '2'
        elif code.startswith('8'):
            return '0'
        else:
            return '-'



    def one(self,code = '600733'):
        # 歌尔
        # code = '600733'
        # 大位
        # code = '600589'
        # 北汽
        # code = '002241'
        print(code)
        try:
            info = self.Model.getOne("select * from stock where code = '{}'".format(code))
            secid = '{}.{}'.format(info['market'], info['code'])
        except Exception as e:
            secid = '{}.{}'.format('0', code)

        sotck_info = self.east_web.get_info(secid, 'f57,f43:2:,f116:8:,f117:8:,f170:2:%,f40:4:,f20:4:')
        # sotck_day_info = self.east_web.get_day_info(secid)
        #
        sotck_days_info = self.east_web.get_days_info(secid)

        print(sotck_days_info)
        sys.exit()
        return sotck_info

    def today(self):
        # 获取当前日期和时间
        now = int(time.time())
        # 格式化日期为 'YYYY-MM-DD' 格式
        today_time = time.strftime("%Y%m%d", time.localtime(now))
        result = self.dbk_web.day_time(today_time)
        print(result['data'])

    def day_time(self,day_num = 2):
        for i in range(int(time.time())-86400*day_num, int(time.time())+86400, 86400):
            day = time.strftime("%Y%m%d", time.localtime(i))
            result = self.dbk_web.day_time(day)
            if result['status']:
                for data in result['data']:
                    for info in data['info']:
                        info['day_time'] = day
                        info['top_num'] = data['top']
                        stock_info = self.one(info['code'])
                        info['price'] = stock_info[1]
                        info['market_price'] = stock_info[2]
                        info['flow_price'] = stock_info[3]
                        print(info)
                        self.save('stock_dbk',info)

def init():
    return dbk()

if __name__ == '__main__':
    obj = dbk()