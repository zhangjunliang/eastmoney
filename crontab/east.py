from lib.east_web import east_web

class east(object):

    def __init__(self):
        self.east_web = east_web()

    def my(self,code_list):
        self.east_web.dump([],'my')
        for code in code_list:
            #f58,
            data = self.east_web.get_info(code, 'f57,f43:2:,f170:2:%,f40:4:,f20:4:')
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
    obj = east()