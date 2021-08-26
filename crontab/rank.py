#!/usr/bin/env python
# -*- coding=UTF-8 -*-

from lib.east_web import east_web
from lib.BaseModel import BaseModel
import time
from config import Config
import sys
import datetime
from chinese_calendar import is_workday, is_holiday

class rank(object):

    def __init__(self):
        self.Config = Config()
        self.Model = BaseModel(self.Config.mysql)
        self.east = east_web()
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

    def save_lhb(self):
        updated = datetime.date.today()

        if is_workday(updated) == False:
            print('Error:{} not work...'.format(updated))
            return

        page = 1
        limit = 10
        while True:
            print(page)
            try:
                data = self.east.get_lhb(page, limit, updated)
            except TypeError as e:
                print(repr(e))
                print('over')
                sys.exit()
            except Exception as e:
                continue

            for stock_row in data:
                if stock_row['MARKET'] == 'SZ':
                    market = 0
                else:
                    market = 1

                secids = str(market) + '.' + stock_row['SECURITY_CODE']
                #secids = '0.300847'
                row = self.east.get_info(secids, '')

                if row['f51'] == '-':
                    row['f51'] = 0
                if row['f52'] == '-':
                    row['f52'] = 0
                if row['f44'] == '-':
                    row['f44'] = 0
                if row['f45'] == '-':
                    row['f45'] = 0
                if row['f43'] == '-':
                    row['f43'] = 0
                if row['f170'] == '-':
                    row['f170'] = 0

                is_top = 0
                if row['f43'] == row['f51']:
                    is_top = 1
                elif row['f43'] == row['f52']:
                    is_top = 2
                sql = """INSERT INTO daily_lhb
                        (name,code,market,remark,updated,price,rate,max_price,min_price,top_price,low_price,is_top) 
                        VALUE('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}') 
                   ON DUPLICATE KEY UPDATE 
                        code = VALUES( code ),
                        name = VALUES( name ),
                        market = VALUES( market ),
                        remark = VALUES( remark ),
                        updated = VALUES( updated ),
                        price = VALUES( price ),
                        rate = VALUES( rate ),
                        max_price = VALUES( max_price ),
                        min_price = VALUES( min_price ),
                        top_price = VALUES( top_price ),
                        low_price = VALUES( low_price ),
                        is_top = VALUES( is_top )
                """.format(row['f58'],
                    row['f57'],
                    row['f107'],
                    stock_row['EXPLAIN'],
                    updated,
                    self.east._field_type(row['f43'], 2, ''),
                    self.east._field_type(row['f170'], 2, ''),
                    self.east._field_type(row['f51'], 2, ''),
                    self.east._field_type(row['f52'], 2, ''),
                    self.east._field_type(row['f44'], 2, ''),
                    self.east._field_type(row['f45'], 2, ''),
                    is_top)
                self.Model.update_One(sql)
            page = page + 1

    def save_lhb_list(self):
        updated = datetime.date.today()
        if is_workday(updated) == False:
            print('Error:{} not work...'.format(updated))
            return

        page = 0
        limit = 100
        is_stop = True
        while is_stop:
            data = self.Model.getAll("SELECT * FROM daily_lhb WHERE updated = '{}' LIMIT {},{}".format(updated, limit * page, limit))
            page = page + 1
            print(len(data))
            for stock_row in data:
                print(stock_row['code'])
                buy_list = self.east.get_lhb_buy(stock_row['code'], updated, False)
                for buy_row in buy_list:
                    sql = """INSERT INTO daily_lhb_list
                                           (`code`, `updated`, `department_code`, `department_name`, `net`, `buy`, `sell`, `is_buy`)
                                           VALUE('{}','{}','{}','{}','{}','{}','{}','{}') 
                                      ON DUPLICATE KEY UPDATE 
                                           code = VALUES( code ),
                                           updated = VALUES( updated ),
                                           department_code = VALUES( department_code ),
                                           department_name = VALUES( department_name ),
                                           net = VALUES( net ),
                                           buy = VALUES( buy ),
                                           sell = VALUES( sell ),
                                           is_buy = VALUES( is_buy )
                                   """.format(stock_row['code'],
                                              updated,
                                              buy_row['department_code'],
                                              buy_row['department_name'],
                                              buy_row['net'],
                                              buy_row['buy'],
                                              buy_row['sell'],
                                              1)
                    self.Model.update_One(sql)
                sell_list = self.east.get_lhb_sell(stock_row['code'], updated, False)
                for sell_row in sell_list:
                    sql = """INSERT INTO daily_lhb_list
                                           (`code`, `updated`, `department_code`, `department_name`, `net`, `buy`, `sell`, `is_buy`)
                                           VALUE('{}','{}','{}','{}','{}','{}','{}','{}') 
                                      ON DUPLICATE KEY UPDATE 
                                           code = VALUES( code ),
                                           updated = VALUES( updated ),
                                           department_code = VALUES( department_code ),
                                           department_name = VALUES( department_name ),
                                           net = VALUES( net ),
                                           buy = VALUES( buy ),
                                           sell = VALUES( sell ),
                                           is_buy = VALUES( is_buy )
                                   """.format(stock_row['code'],
                                              updated,
                                              sell_row['department_code'],
                                              sell_row['department_name'],
                                              sell_row['net'],
                                              sell_row['buy'],
                                              sell_row['sell'],
                                              0)
                    self.Model.update_One(sql)

            if len(data) < limit:
                print('over')
                sys.exit()

def init():
    return rank()

if __name__ == '__main__':
    obj = rank()