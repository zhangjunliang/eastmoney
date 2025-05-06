#!/usr/bin/env python
# -*- coding=UTF-8 -*-

from lib.dbk_web import dbk_web
from lib.east_web import east_web
from lib.BaseModel import BaseModel
import lib.public as public
import time
from config import Config
import sys
import datetime
from loguru import logger
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



    def one(self,code = '000627'):
        # 歌尔
        # code = '600733'
        # 大位
        # code = '600589'
        # 北汽
        # code = '002241'
        # code  = '000766'
        # print(code)
        try:
            info = self.Model.getOne("select * from stock where code = '{}'".format(code))
            secid = '{}.{}'.format(info['market'], info['code'])
        except Exception as e:
            secid = '{}.{}'.format('0', code)

        stock_info = self.east_web.get_info(secid, 'f57,f43:2:,f116:8:,f117:8:,f170:2:%,f40:4:,f20:4:')

        # stock_history_data = self.Model.getAll("select * from stock_history where code = '{}' order by day_time desc ".format(str(info['code'])))

        return stock_info

    def get_one(self, code='600733'):
        try:
            info = self.Model.getOne("select * from stock where code = '{}'".format(code))
            secid = '{}.{}'.format(info['market'], info['code'])
        except Exception as e:
            secid = '{}.{}'.format('0', code)

        stock_info = self.east_web.get_info(secid, 'f57,f43:2:,f116:8:,f117:8:,f170:2:%,f40:4:,f20:4:')
        return stock_info

    def today(self):
        # 获取当前日期和时间
        now = int(time.time())
        # 格式化日期为 'YYYY-MM-DD' 格式
        today_time = time.strftime("%Y%m%d", time.localtime(now))
        result = self.dbk_web.day_time(today_time)
        print(result['data'])

    def day_time(self,day_num = 3):
        for i in range(int(time.time())-86400*day_num, int(time.time())+86400, 86400):
            day = time.strftime("%Y%m%d", time.localtime(i))
            result = self.dbk_web.day_time(day)
            if result['status']:
                for data in result['data']:
                    for info in data['info']:
                        info['day_time'] = day
                        info['top_num'] = data['top']
                        stock_dbk_data = self.Model.getOne("select * from stock_dbk where code = '{}' and day_time = '{}'".\
                               format(info['code'],day))
                        # 类型1 写入 2 更新 3 已更新跳过
                        if stock_dbk_data != None:
                            task_type = 2
                            logger.info('day:{},code:{},task_type:{} '.format(day, info['code'], task_type))
                            continue
                        else:
                            task_type = 1
                            stock_info = self.get_one(info['code'])
                            info['price'] = stock_info[1]
                            info['market_price'] = stock_info[2]
                            info['flow_price'] = stock_info[3]
                            self.save('stock_dbk',info)
                            logger.info('day:{},code:{},task_type:{} '.format(day, info['code'], task_type))

def init():
    return dbk()

if __name__ == '__main__':
    obj = dbk()