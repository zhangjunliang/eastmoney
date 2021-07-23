#!/usr/bin/env python
# -*- coding=UTF-8 -*-
from lib.east_web import east_web
from lib.BaseModel import BaseModel
import time
from config import Config
import sys
import datetime
from chinese_calendar import is_workday, is_holiday

class stock(object):

    def __init__(self):
        self.Config = Config()
        self.Model = BaseModel(self.Config.mysql)
        self.east = east_web()
        self._t = round(time.time() * 1000)

    ## 保存所有股票信息
    def save_stock(self):
        updated = datetime.date.today()
        if is_workday(updated) == False:
            print('Error:{} not work...'.format(updated))
            return

        print('start')
        page = 1
        while True:
            print(page)
            self.east.delay_sleep()
            num = 100
            url = 'https://push2.eastmoney.com/api/qt/clist/get?ut=7eea3edcaed734bea9cbfc24409ed989&pn={}&pz={}&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2&fields=f14,f12,f2,f3,f13&_={}' \
                .format(page, num, self._t)
            try:
                result = self.east._get('all', url, 'f14,f12,f13,f2,f3',is_print=False)
            except TypeError as e:
                print(repr(e))
                print('over')
                sys.exit()
            except Exception as e:
                break

            for row in result:
                if row[3] == '-':
                    row[3] = 0
                if row[4] == '-':
                    row[4] = 0

                sql = """
                    INSERT INTO stock(name,code,market,price,rate) VALUE('{}','{}','{}','{}','{}') ON DUPLICATE KEY UPDATE 
                    code = VALUES( code ),name = VALUES( name ),market = VALUES( market ),price = VALUES( price ),rate = VALUES( rate )
                """.format(row[0], row[1], row[2], row[3], row[4])
                self.Model.update_One(sql)
            page = page + 1

    def save_stock_bk(self):

        updated = datetime.date.today()
        if is_workday(updated) == False:
            print('Error:{} not work...'.format(updated))
            return

        page = 0
        limit = 100
        clear_sql = "DELETE FROM stock_bk WHERE bk_code IN ( 'BK0816', 'BK0815', 'BK0817')"
        self.Model.update_One(clear_sql)
        while True:
            print(page)
            self.east.delay_sleep()
            data = self.Model.getAll("select * from stock limit {},{}".format(limit * page, limit))
            if len(data) < 1:
                print('over')
                sys.exit()
            for stock_row in data:
                secids = str(stock_row['market']) + '.' + stock_row['code']
                # print(secids)
                try:
                    bk_data = self.east.get_stock_bk(secids, '')
                except Exception as e:
                    print(e)
                    page = page - 1
                    break;

                for row in bk_data:
                    sql = """INSERT INTO stock_bk
                               (name,code,market,bk_name,bk_code) 
                               VALUE('{}','{}','{}','{}','{}') 
                          ON DUPLICATE KEY UPDATE 
                               name = VALUES( name ),
                               code = VALUES( code ),
                               market = VALUES( market ),
                               bk_name = VALUES( bk_name ),
                               bk_code = VALUES( bk_code )
                           """.format(stock_row['name'], stock_row['code'], stock_row['market'], row['f14'], row['f12'])
                    self.Model.update_One(sql)
            page = page + 1

    def save_daily_top(self):

        updated = datetime.date.today()
        if is_workday(updated) == False:
            print('Error:{} not work...'.format(updated))
            return

        page = 0
        limit = 100
        while True:
            data = self.Model.getAll("select * from stock limit {},{}".format(limit * page, limit))
            print(page)
            if len(data) < 1:
                print('over')
                sys.exit()
            for stock_row in data:
                #
                if (stock_row['rate'] < 9.5 and stock_row['rate'] > 6) \
                    or (stock_row['rate'] < 4.5 and stock_row['rate'] > -4.5) \
                    or (stock_row['rate'] > -9.5 and stock_row['rate'] < -6):
                    continue

                secids = str(stock_row['market']) + '.' + stock_row['code']
                #secids = '0.300847'
                try:
                    row = self.east.get_info(secids, '')
                except Exception as e:
                    print(e)
                    page = page - 1
                    break;

                if row['f170'] == 0 or row['f51'] == '-' or row['f52'] == '-':
                    continue
                is_top = 0
                if row['f43'] == row['f51']:
                    is_top = 1
                elif row['f43'] == row['f52']:
                    is_top = 2
                else:
                    continue
                sql = """INSERT INTO daily_top
                        (name,code,market,updated,price,rate,max_price,min_price,top_price,low_price,is_top) 
                        VALUE('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}') 
                   ON DUPLICATE KEY UPDATE 
                        code = VALUES( code ),
                        name = VALUES( name ),
                        market = VALUES( market ),
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

    def save_daily_hot(self):

        updated = datetime.date.today()

        data = self.east.get_hot('',False)


        for index,stock_row in enumerate(data):
            secids = str(stock_row['f13']) + '.' + stock_row['f12']
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
            sql = """INSERT INTO daily_hot
                    (name,code,market,rank,updated,price,rate,max_price,min_price,top_price,low_price,is_top) 
                    VALUE('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}') 
               ON DUPLICATE KEY UPDATE 
                    code = VALUES( code ),
                    name = VALUES( name ),
                    market = VALUES( market ),
                    rank = VALUES( rank ),
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
                index + 1,
                updated,
                self.east._field_type(row['f43'], 2, ''),
                self.east._field_type(row['f170'], 2, ''),
                self.east._field_type(row['f51'], 2, ''),
                self.east._field_type(row['f52'], 2, ''),
                self.east._field_type(row['f44'], 2, ''),
                self.east._field_type(row['f45'], 2, ''),
                is_top)
            self.Model.update_One(sql)


def init():
    return stock()

if __name__ == '__main__':
    obj = stock()