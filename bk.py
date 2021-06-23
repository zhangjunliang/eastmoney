from lib.east_web import east_web
import sys

if __name__ == '__main__':
    east_web = east_web()
    name = 'b:BK{}'.format(str(sys.argv[1]))
    print(name)
    data = east_web.get_bk_stock(name, 'f14,f12,f2:2,f3:2:%')
    east_web.dump(data, name)