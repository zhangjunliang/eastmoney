from lib.east_web import east_web
from lib.BaseModel import BaseModel
import time
from config import Config
import sys
import datetime
from chinese_calendar import is_workday, is_holiday

class info(object):

    def __init__(self):
        self.Config = Config()
        self.Model = BaseModel(self.Config.mysql)
        self.east = east_web()
        self._t = round(time.time() * 1000)

    def daily_info(self,updated = None):

        if updated == None:
            updated = datetime.date.today()

        print(updated)

        sql = "select SUM(IF(is_top = 1,1,0)) as top_num,SUM(IF(is_top = 2,1,0)) as low_num from daily_top as d where d.updated = '{}'".format(updated)
        data = self.Model.getOne(sql)

        stop_sql = "select count(*) as stop_num from stock  where rate = 0 and price = 0"
        stop_data = self.Model.getOne(stop_sql)

        str = "top:{}|low:{}|stop:{}".format(data['top_num'],data['low_num'],stop_data['stop_num'])


        rate_sql = "select fromat_rate(rate) as rate,count(*) as num from stock  where rate != 0 and price != 0 group by fromat_rate(rate) order by fromat_rate(rate)"
        rate_data = self.Model.getAll(rate_sql)
        for row in rate_data:
            print(row)

        print(str)

    def top_bk_num(self, updated=None):
        if updated == None:
            updated = datetime.date.today()
        print(updated)
        #  having num > 1
        sql = """
            select *,count(*) num from (
            select b.bk_name,b.bk_code  from daily_top as d inner join stock_bk as b on d.code = b.code where d.is_top = 1 
            and b.bk_code not in (select bk_code from bk where weight < 0) 
            and d.updated >= '{}'

            union all 

            select b.bk_name,b.bk_code  from daily_hot as d inner join stock_bk as b on d.code = b.code where d.is_top = 1 
            and b.bk_code not in (select bk_code from bk where weight < 0) 
            and d.updated >= '{}'

            union all

            select b.bk_name,b.bk_code  from daily_lhb as d inner join stock_bk as b on d.code = b.code where d.is_top = 1 
            and b.bk_code not in (select bk_code from bk where weight < 0) 
            and d.updated >= '{}'
            ) as t group by t.bk_code order by num
        """.format(updated, updated, updated)
        data = self.Model.getAll(sql)
        for row in data:
            str = "{}|{}|{}".format(row['bk_name'], row['bk_code'], row['num'])
            print(str)

    def top_bk(self, updated=None):
        if updated == None:
            updated = datetime.date.today()
        print(updated)
        #  having num > 1
        sql = """
            select *,count(*) num from (
            select b.bk_name,b.bk_code  from daily_top as d inner join stock_bk as b on d.code = b.code where d.is_top = 1 
            and b.bk_code not in (select bk_code from bk where weight < 0) 
            and d.updated = '{}'
            
            union all 
            
            select b.bk_name,b.bk_code  from daily_hot as d inner join stock_bk as b on d.code = b.code where d.is_top = 1 
            and b.bk_code not in (select bk_code from bk where weight < 0) 
            and d.updated = '{}'
            
            union all
            
            select b.bk_name,b.bk_code  from daily_lhb as d inner join stock_bk as b on d.code = b.code where d.is_top = 1 
            and b.bk_code not in (select bk_code from bk where weight < 0) 
            and d.updated = '{}'
            ) as t group by t.bk_code order by num
        """.format(updated,updated,updated)
        data = self.Model.getAll(sql)
        for row in data:
            str = "{}|{}|{}".format(row['bk_name'], row['bk_code'], row['num'])
            print(str)

    def top_num(self, updated=None):

        if updated == None:
            updated = datetime.date.today()
        print(updated)
        #  having num > 1
        sql = """
            select d.*,count(*) as num from daily_top as d  where d.is_top = 1 
            and d.updated >= '{}' group by d.code
            order by num 
        """.format(updated)
        data = self.Model.getAll(sql)
        for row in data:
            str = "{}|{}|{}".format(row['name'], row['code'], row['num'])
            print(str)



    def top_diff(self,updated = None):

        if updated == None:
            updated = datetime.date.today()
        print(updated)

        sql = """select d.updated,ROUND((s.price - d.price)/d.price*100,2)  as change_rage,s.*
                from daily_top as d left join stock as s on d.code = s.code 
                where d.updated = '{}' order by change_rage desc
        """.format(updated)
        data = self.Model.getAll(sql)
        for row in data:
            str = "{}|{}|{}".format(row['name'], row['code'], row['change_rage'])
            print(str)

    def top(self):
        sql = 'select d.*,count(*) as num from daily_top as d  where d.is_top = 1 group by d.code order by num'
        data = self.Model.getAll(sql)
        for row in data:
            str = "{}|{}|{}".format(row['name'], row['code'],row['num'])
            print(str)


def init():
    return info()

if __name__ == '__main__':
    obj = info()