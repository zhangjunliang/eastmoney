#!/usr/bin/env python
# -*- coding=UTF-8 -*-

from lib.east_web import east_web
from lib.BaseModel import BaseModel
import time
from config import Config
import sys
import datetime
from chinese_calendar import is_workday, is_holiday
import lib.public as public
from loguru import logger

class bk(object):

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

    def save_bk(self):
        # updated = datetime.date.today()
        # if is_workday(updated) == False:
        #     print('Error:{} not work...'.format(updated))
        #     sys.exit()

        page = 1
        limit = 100

        snatch_time = time.strftime('%Y-%m-%d %H:%M:%S')
        diff_time = public.date_to_timestamp(snatch_time) - public.date_to_timestamp(time.strftime('%Y-%m-%d 15:00:00'))
        # diff_time = 6 * 60 * 60

        while True:
            print(page)
            try:
                result = self.east.get_bk(page, limit, '', False)
            except TypeError as e:
                print(repr(e))
                print('over')
                sys.exit()
            except Exception as e:
                continue

            for row in result:

                bk_code = row['f12']
                bk_data = self.Model.getOne("select * from bk where bk_code = '{}'".format(str(bk_code)))

                # 类型1 写入 2 更新 3 已更新跳过
                task_type = 1
                if bk_data != None:

                    if bk_data['snatch_time'] == "0000-00-00 00:00:00":
                        bk_snatch_time = 0
                    else:
                        bk_snatch_time = public.date_to_timestamp(str(bk_data['snatch_time']))

                    if public.date_to_timestamp(snatch_time) - bk_snatch_time > diff_time:
                        task_type = 2
                    else:
                        task_type = 3

                logger.info('page:{},code:{},task_type:{} '.format(page, bk_code, task_type))
                if task_type == 3:
                    continue

                secid = '{}.{}'.format('90',row['f12'])
                history_info = self.east.get_day_info(secid, lmt=20)
                for day_info in history_info:
                    history_data = self.Model.getOne("select * from history where code = '{}' and 'day_time' = '{}' " \
                                                     .format(row['f12'], day_info[0]))
                    if history_data == None:
                        save_data = {
                            'name': row['f14'],
                            'code': row['f12'],
                            'day_time': day_info[0],
                            'price': day_info[2],
                            'price_start': day_info[1],
                            'price_high': day_info[3],
                            'price_low': day_info[4],
                            'price_rate': day_info[9],
                            'rate': day_info[8],
                            'rate_diff': day_info[7],
                            'rate_change': day_info[10],
                            'deal_amount': round(float(day_info[5]) / 10000, 2),
                            'deal_price': round(float(day_info[6]) / 10000, 2)
                        }
                        self.Model.save('history', save_data)

                price_5 = public.avg(history_info, num=5, field=2)
                price_10 = public.avg(history_info, num=10, field=2)
                price_20 = public.avg(history_info, num=20, field=2)

                bk_id = int(row['f12'][2:])
                bk_type = row['f19']

                save_data = {
                    'id' : bk_id,
                    'bk_name': row['f14'],
                    'bk_code': row['f12'],
                    'bk_type': bk_type,
                    'rate': row['f3'],
                    'rate_3': row['f127'],
                    'price': row['f2'],
                    'price_5': price_5,
                    'price_10': price_10,
                    'price_20': price_20,
                    'is_option': '0',
                    'weight': '0',
                    'snatch_time': snatch_time,
                }

                if task_type == 1:
                    self.Model.save(table='bk', data=save_data)
                else:

                    del save_data['is_option']
                    del save_data['weight']

                    where_data = {
                        'bk_code': bk_code
                    }
                    self.Model.update(table='bk', data=save_data, where_data=where_data,limit=1)

            page = page + 1



def init():
    return bk()

if __name__ == '__main__':
    obj = bk()