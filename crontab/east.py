from lib.east_web import east_web
from lib.BaseModel import BaseModel
from config import Config
import sys

class east(object):

    def __init__(self):
        self.Config = Config()
        self.Model = BaseModel(self.Config.mysql)
        self.east_web = east_web()

    def code(self,code):
        info = self.Model.getOne("select * from stock where code = '{}'".format(code))
        secid = '{}.{}'.format(info['market'], info['code'])
        data = self.east_web.get_info(secid, 'f57,f43:2:,f170:2:%,f40:4:,f20:4:')
        self.east_web.dump(data)

    def one(self,code):
        info = self.Model.getOne("select * from stock where code = '{}'".format(code))
        secid = '{}.{}'.format(info['market'], info['code'])
        data = self.east_web.get_info(secid, 'f57,f43:2:,f170:2:%,f40:4:,f20:4:')
        self.east_web.dump(data)
        bk_data = self.east_web.get_stock_bk(secid, 'f14,f12,f3:2:%,f128,f140,f136:2:%')
        self.east_web.dump(bk_data)

    def my(self,weight = None):

        if weight == None:
            sql = "select * from stock where weight > 0 order by weight"
        else:
            sql = "select * from stock where weight > {} order by weight".format(weight)

        data = self.Model.getAll(sql)
        self.east_web.dump([],'my')
        for row in data:
            secid = '{}.{}'.format(row['market'],row['code'])
            data = self.east_web.get_info(secid, 'f57,f43:2:,f170:2:%,f40:4:,f20:4:')
            self.east_web.dump(data)

    def top(self):
        self.east_web.get_stock_top()

    def bk(self,params):
        name = 'b:BK{}'.format(params)
        data = self.east_web.get_bk_stock(name, 'f14,f12,f2:2,f3:2:%')
        self.east_web.dump(data, name)

    def info(self,fun):
        if fun == 'help':
            self.east_web.dump(self.east_web.methods())
        else:
            do = getattr(self.east_web, 'get_' + fun)
            do()

def init():
    return east()

if __name__ == '__main__':
    init = east()