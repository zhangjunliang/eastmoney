#!/usr/bin/env python
# -*- coding=UTF-8 -*-
from lib.east_web import east_web
from lib.BaseModel import BaseModel
import time
from config import Config
import sys
import datetime
from chinese_calendar import is_workday, is_holiday

class lottery(object):

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



    def save_ssq(self):
        data = self.east.get_lottery('ssq',100,False)
        for row in data:
            field_str = '`,`'.join(str(i) for i in row)
            field_val = ','.join('%s' for i in row)
            field_data = list(row[i] for i in row)
            sql = """INSERT IGNORE INTO lottery(`{}`)  VALUE({})""".format(field_str, field_val)
            self.Model.update_One(sql,field_data)
        print('over nums：{}'.format(len(data)))

    def guess(self):
        blue_start = 1
        blue_end = 8
        last_code = 1
        blue_limit = 40
        red_limit = 40
        blue_sql = '''
SELECT * FROM (
	SELECT blue1,COUNT(*) AS nums FROM 
	(
		SELECT blue1 from lottery WHERE blue1 BETWEEN {blue_start} AND {blue_end} AND `type` = 'ssq' ORDER BY `code` LIMIT {last_code},{limit} 
	) t
	WHERE blue1 NOT IN (
		SELECT * FROM (SELECT blue1 AS red from lottery WHERE `type` = 'ssq' ORDER BY `code` DESC LIMIT {code},1) l1
	)
	GROUP BY blue1 ORDER BY nums DESC LIMIT 1,3
) r ORDER BY r.nums desc;
        '''.format(blue_start = blue_start,blue_end = blue_end,last_code=last_code,code=last_code-1,limit=blue_limit)


        red_sql = '''
SELECT red,nums FROM (
	SELECT red,COUNT(*) AS nums FROM 
	(
		SELECT * FROM (SELECT red1 as red from lottery WHERE `type` = 'ssq' ORDER BY `code` DESC LIMIT {last_code},{limit}) t1
		UNION all
		SELECT * FROM (SELECT red2 as red from lottery WHERE `type` = 'ssq' ORDER BY `code` DESC LIMIT {last_code},{limit}) t2
		UNION all
		SELECT * FROM (SELECT red3 as red from lottery WHERE `type` = 'ssq' ORDER BY `code` DESC LIMIT {last_code},{limit}) t3
		UNION all
		SELECT * FROM (SELECT red4 as red from lottery WHERE `type` = 'ssq' ORDER BY `code` DESC LIMIT {last_code},{limit}) t4
		UNION all
		SELECT * FROM (SELECT red5 as red from lottery WHERE `type` = 'ssq' ORDER BY `code` DESC LIMIT {last_code},{limit}) t5
		UNION all
		SELECT * FROM (SELECT red6 as red from lottery WHERE `type` = 'ssq' ORDER BY `code` DESC LIMIT {last_code},{limit}) t6	
	) t 
	WHERE red NOT IN (
		SELECT * FROM (SELECT red1 AS red from lottery WHERE `type` = 'ssq' ORDER BY `code` DESC LIMIT {code},1) l1
		UNION ALL
		SELECT * FROM (SELECT red2 AS red from lottery WHERE `type` = 'ssq' ORDER BY `code` DESC LIMIT {code},1) l2 
		UNION ALL
		SELECT * FROM (SELECT red3 AS red from lottery WHERE `type` = 'ssq' ORDER BY `code` DESC LIMIT {code},1) l3
		UNION ALL
		SELECT * FROM (SELECT red4 AS red from lottery WHERE `type` = 'ssq' ORDER BY `code` DESC LIMIT {code},1) l4
		UNION ALL
		SELECT * FROM (SELECT red5 AS red from lottery WHERE `type` = 'ssq' ORDER BY `code` DESC LIMIT {code},1) l5
		UNION ALL
		SELECT * FROM (SELECT red6 AS red from lottery WHERE `type` = 'ssq' ORDER BY `code` DESC LIMIT {code},1) l6
	)		
	GROUP BY red ORDER BY nums DESC LIMIT 1,6
) r ORDER BY r.red;
                '''.format(last_code=last_code,code=last_code-1,limit=red_limit)

        blue_list = self.Model.getAll(blue_sql)
        blue_str = ','.join(str(i['blue1']) for i in blue_list)

        red_list = self.Model.getAll(red_sql)
        red_str = ','.join(str(i['red']) for i in red_list)

        print(red_str,blue_str)

def init():
    return lottery()

if __name__ == '__main__':
    obj = lottery()