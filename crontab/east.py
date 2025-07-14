#!/usr/bin/env python
# -*- coding=UTF-8 -*-

from lib.east_web import east_web
from lib.BaseModel import BaseModel
from config import Config
import lib.public as public
import sys

class east(object):

    def __init__(self):
        self.Config = Config()
        self.Model = BaseModel(self.Config.mysql)
        self.east_web = east_web()

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

    def kzc_code(self,code):
        secid = code
        #f57,
        data = self.east_web.get_info(secid, 'f43:3:,f170:2:%,f40:4:,f20:4:')
        self.east_web.dump(data)

    def code(self,code):
        info = self.Model.getOne("select * from stock where code = '{}'".format(code))
        secid = '{}.{}'.format(info['market'], info['code'])
        #f57,
        data = self.east_web.get_info(secid, 'f43:2:,f170:2:%,f40:4:,f20:4:')

        data.append(info['price_5'])
        data.append(info['flow_price'])
        data.append(int(info['price'] >= info['price_5'] >= info['price_10'] >= info['price_20']))

        self.east_web.dump(data)

    def fund(self,code = '159707'):
        info = self.Model.getOne("select * from stock where code = '{}'".format(code))
        secid = '{}.{}'.format(info['market'], info['code'])
        #f57,
        data = self.east_web.get_fund(secid, 'f43:3:,f170:2:%,f40:4:,f20:4:')
        self.east_web.dump(data)

    def one(self,code):
        info = self.Model.getOne("select * from stock where code = '{}'".format(code))
        secid = '{}.{}'.format(info['market'], info['code'])
        data = self.east_web.get_info(secid, 'f57,f43:2:,f170:2:%,f40:4:,f20:4:')
        self.east_web.dump(data)
        bk_data = self.east_web.get_stock_bk(secid, 'f14,f12,f3:2:%,f128,f140,f136:2:%')
        self.east_web.dump(bk_data)

    def my(self,is_select = None):

        if is_select == None:
            sql = "select * from stock where is_select > 0 order by weight"
        else:
            sql = "select * from stock where is_select > {} order by weight".format(is_select)

        data = self.Model.getAll(sql)
        self.east_web.dump([],'')
        for row in data:
            secid = '{}.{}'.format(row['market'],row['code'])

            if row['type'] == 1:
                f = 'f57,f43:2:,f170:2:%,f40:4:,f20:4:'
                f = 'f43:2:,f170:2:%,f40:4:,f20:4:'
                data = self.east_web.get_info(secid, f)

                bk_sql = 'select count(*) as num from stock_bk where code = {} and bk_code = "BK0596" limit 1'.format(
                    row['code'])
                stock_bk_data = self.Model.getOne(bk_sql)

                data.append('L{}'.format(int(row['flow_price'])))
                data.append('Q{}'.format(int(row['price'] >= row['price_5'] >= row['price_10'] >= row['price_20'])))
                data.append('F{}'.format(int(row['dividend_ratio'] > 0)))
                data.append('R{}'.format(stock_bk_data['num']))

                hy_type = self.east_web.get_peak_stock(type = 2,is_print=False)
                dq_type = self.east_web.get_db_bk(code = row['code'])

                d_tag = '{}{}'.format(dq_type['bk_name'][0:1],hy_type.get(dq_type['bk_name'],'0'))
                data.append(d_tag)

            elif row['type'] == 2:
                f = 'f57,f43:3:,f170:2:%,f40:4:,f20:4:'
                f = 'f43:3::3,f170:2:%,f40:4:,f20:4:'
                data = self.east_web.get_fund(secid, f)
            else:
                data = []

            self.east_web.dump(data)

    def top(self):
        self.east_web.get_stock_top()

    def bk(self,params):
        name = 'b:BK{}'.format(params)
        data = self.east_web.get_bk_stock(name, 'f14,f12,f2:2,f3:2:%')
        self.east_web.dump(data, name)

    def peak(self,params = 1):
        data = self.east_web.get_peak_stock(type = params,is_print=True)

    def info(self,fun):
        if fun == 'help':
            self.east_web.dump(self.east_web.help())
        else:
            do = getattr(self.east_web, 'get_' + fun)
            do()

def init():
    return east()

if __name__ == '__main__':
    init = east()