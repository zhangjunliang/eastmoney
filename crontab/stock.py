#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import os

from lib.east_web import east_web
from lib.BaseModel import BaseModel
import time
from config import Config
import sys
import datetime
from chinese_calendar import is_workday, is_holiday
from concurrent.futures import as_completed
import concurrent.futures
import platform
import lib.public as public
from loguru import logger
from openpyxl import Workbook

# 加上这行代码即可，关闭安全请求警告
# requests.packages.urllib3.disable_warnings()

class stock(object):

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

    def save_stock(self):
        page = 1
        num = 100
        end_page = 5300/num
        with concurrent.futures.ThreadPoolExecutor(max_workers = 1) as executor_m3u8:
            while True:
                obj_list = []
                obj = executor_m3u8.submit(self.save_stock_one, page = page, num = num)
                obj_list.append(obj)
                page = page + 1
                if page > end_page:
                    print('save end ok:{}'.format(str(page)))
                    sys.exit()

        # while True:
        #     self.save_stock_one(page = page, num = num)
        #     page = page + 1
        #     if page > end_page:
        #         print('save end ok:{}'.format(str(page)))
        #         sys.exit()

    def save_stock_history(self):
        #  where code = '002241'
        data = self.Model.getAll("select * from stock")
        logger.info('start')
        for stock_row in data:
            secids = str(stock_row['market']) + '.' + str(stock_row['code'])
            logger.info('code:{}'.format(secids))
            today_day = time.strftime('%Y-%m-%d')
            stock_history_data = self.Model.getOne(
                "select * from stock_history where code = '{}' and 'day_time' = '{}' " \
                .format(stock_row['code'], today_day))
            if stock_history_data != None:
                logger.info('exist:{}.today_day'.format(stock_row['code'], today_day))
                continue

            history_info = self.east.get_day_info(secids)
            for day_info in history_info:
                stock_history_data = self.Model.getOne("select * from stock_history where code = '{}' and 'day_time' = '{}' " \
                     .format(stock_row['code'],day_info[0]))
                if stock_history_data == None:
                    save_data = {
                        'name': stock_row['name'],
                        'code': stock_row['code'],
                        'day_time': day_info[0],
                        'price': day_info[2],
                        'price_start': day_info[1],
                        'price_high': day_info[3],
                        'price_low': day_info[4],
                        'price_rate': day_info[9],
                        'rate': day_info[8],
                        'rate_diff': day_info[7],
                        'rate_change': day_info[10],
                        'deal_amount': round(float(day_info[5]) / 10000,2),
                        'deal_price': round(float(day_info[6]) / 10000,2)
                    }
                    self.Model.save('stock_history',save_data)
        logger.info('end')

    ## 保存所有股票信息
    def save_stock_one(self,page = 1,num = 10):
        diff_time = 6*60*60

        snatch_time = time.strftime('%Y-%m-%d %H:%M:%S')

        logger.info('start:{}'.format(str(page)))

        #self.east.delay_sleep()
        url = 'https://push2.eastmoney.com/api/qt/clist/get?ut=7eea3edcaed734bea9cbfc24409ed989&pn={}&pz={}&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2&fields=f14,f12,f2,f3,f13&_={}' \
            .format(page, num, self._t)

        try:
            result = self.east._get('all', url, 'f14,f12,f13,f2,f3',is_print=False)
        except Exception as e:
            print('page:{},error:{}'.format(str(page),str(e)))
            return True

        for row in result:
            if row[3] == '-':
                row[3] = 0
            if row[4] == '-':
                row[4] = 0

            code = row[1]
            secid = '{}.{}'.format(str(row[2]),str(code))
            stock_data = self.Model.getOne("select * from stock where code = '{}'".format(str(code)))
            # 类型1 写入 2 更新 3 已更新跳过
            task_type = 1
            if stock_data != None:

                if stock_data['snatch_time'] == "0000-00-00 00:00:00":
                    stock_snatch_time = 0
                else:
                    stock_snatch_time = public.date_to_timestamp(str(stock_data['snatch_time']))

                if public.date_to_timestamp(snatch_time) - stock_snatch_time > diff_time:
                    task_type = 2
                else:
                    task_type = 3

            logger.info('page:{},code:{},task_type:{} '.format(page,code,task_type))
            if task_type == 3:
                continue

            stock_info = self.east.get_info(secid, 'f57,f43:2:,f116:8:,f117:8:,f170:2:%,f40:4:,f20:4:')

            market_info = public.get_market_info(row[1], row[0],market = row[2],price = row[3])

            code_str = '{}.{}'.format(row[1],market_info['market_str'])
            dividend_info = self.east.get_dividend_info(code_str)
            data_info = self.east.get_data_info(code_str)

            history_info = self.east.get_day_info(secid,lmt = 20)

            price_5 = public.avg(history_info, num = 5,field = 2)
            price_10 = public.avg(history_info, num = 10, field = 2)
            price_20 = public.avg(history_info, num = 20, field = 2)

            save_data = {
                'name': row[0],
                'code': row[1],
                'type': 1,
                'market': row[2],
                'market_type': market_info['market_type'],
                'price': row[3],
                'market_price': stock_info[2],
                'flow_price': stock_info[3],
                'rate': row[4],
                'price_5': price_5,
                'price_10': price_10,
                'price_20': price_20,
                'dividend_ratio': dividend_info['dividend_ratio'],
                'dividend_price': '0',
                'gross_price': data_info['gross_price'],
                'profit_price': data_info['profit_price'],
                'gross_rate': data_info['gross_rate'],
                'profit_rate': data_info['profit_rate'],
                'weight': market_info['weight'],
                'snatch_time': snatch_time,
            }
            if task_type == 1:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    obj_list = []
                    obj = executor.submit(self.Model.save, table='stock', data=save_data)
                    obj_list.append(obj)
            else:
                where_data = {
                    'code': code
                }
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    obj_list = []
                    obj = executor.submit(self.Model.update, table='stock', data=save_data ,where_data = where_data , limit = 1)
                    obj_list.append(obj)

        print('end:{}'.format(str(page)))
        return True

    def save_stock_dividend(self):
        #   where code = 603538 order by id desc
        data = self.Model.getAll("select * from stock order by id desc")
        logger.info('start')
        for stock_row in data:
            market_info = public.get_market_info(stock_row['code'], stock_row['name'], market=stock_row['market'])
            code_str = '{}.{}'.format(stock_row['code'], market_info['market_str'])
            secid = '{}.{}'.format(stock_row['market'],stock_row['code'])
            logger.info(code_str)
            dividend_list = self.east.get_dividend_list(code_str,secid)
            if dividend_list == False:
                continue
            # `code`, `dividend_year`, `dividend_num`
            for dividend_info in dividend_list:
                dividend_info_data = self.Model.getOne("select * from stock_dividend where code = '{}' and 'dividend_year' = '{}' and 'dividend_num' = '{}'" \
                     .format(stock_row['code'],dividend_info['dividend_year'],dividend_info['dividend_num']))
                save_data = {
                    'name': stock_row['name'],
                    'code': stock_row['code'],
                    'price': dividend_info['price'],
                    'dividend_year': dividend_info['dividend_year'],
                    'dividend_num': dividend_info['dividend_num'],
                    'dividend_plan': dividend_info['dividend_plan'],
                    'dividend_ratio': dividend_info['dividend_ratio'],
                    'dividend_price': dividend_info['dividend_price'],
                    'dividend_date': dividend_info['dividend_date']
                }
                if dividend_info_data == None:
                    self.Model.save('stock_dividend',save_data)
                else:
                    where_data = {
                        'name': stock_row['name'],
                        'code': stock_row['code'],
                        'price': dividend_info['price']
                    }
                    self.Model.update(table='stock_dividend', data=save_data, where_data=where_data)

        logger.info('end')

    def save_stock_bk(self):
        # updated = datetime.date.today()
        # if is_workday(updated) == False:
        #     print('Error:{} not work...'.format(updated))
        #     sys.exit()

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
                    break

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

    def save_execl(self):

        execl_list = [
            {
                'file' : './file/qs-10.xlsx',
                'where': " is_option = '10' ",
            },
            {
                'file': './file/qs-20.xlsx',
                'where': " is_option = '20' ",
            },
            {
                'file': './file/qs-30.xlsx',
                'where': " is_option = '30' ",
            },
            {
                'file': './file/qs-40.xlsx',
                'where': " is_option = '40' ",
            },
            {
                'file': './file/qs-50.xlsx',
                'where': " is_option = '50' ",
            },
            {
                'file': './file/bz-100.xlsx',
                'where': " weight = '100' ",
            },
            {
                'file': './file/bz-200.xlsx',
                'where': " weight = '200' ",
            }
        ]

        for row in execl_list:
            file = row['file']
            where = row['where']

            try:
                os.remove(file)
            except Exception as e:
                pass

            sql = "select * from stock where {} ".format(where)

            print(sql)

            data = self.Model.getAll(sql)
            wb = Workbook()
            ws = wb.active
            ws.title = "Sheet1"
            ws.append(["代码", "名称"])

            for stock_info in data:
                ws.append([stock_info['code'],stock_info['name']])

            # 保存工作簿到文件
            wb.save(file)

    ## 保存所有基金信息
    def save_fund(self):
        # updated = datetime.date.today()
        # if is_workday(updated) == False:
        #     print('Error:{} not work...'.format(updated))
        #     return

        print('start')
        page = 1
        while True:
            self.east.delay_sleep()
            num = 100
            try:
                result = self.east.get_fund_list(p=page,ps=num)
            except TypeError as e:
                self.last()
                print(repr(e))
                print('over')
                sys.exit()
            except Exception as e:
                continue

            print('page {}:{}'.format(page, len(result)))

            if len(result) < 1:
                sys.exit()

            for row in result:
                item_row = {
                    'name': row[0],
                    'type': 2,
                    'code': row[1],
                    'market': row[4],
                    'price': row[3],
                    'rate': row[2],
                    'is_t0': row[5]
                }
                field_str = '`,`'.join(str(i) for i in item_row)
                field_val = ','.join('%s' for i in item_row)
                field_data = list(item_row[i] for i in item_row)
                field_update = ','.join(' {}=VALUES({}) '.format(str(i),str(i)) for i in item_row)
                sql = """
                    INSERT INTO stock(`{}`) VALUE({}) ON DUPLICATE KEY UPDATE {}
                """.format(field_str,field_val,field_update)
                self.Model.update_One(sql,field_data)

            page = page + 1
    # ========================================
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
                    break

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