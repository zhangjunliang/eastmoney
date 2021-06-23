from lib.east_web import east_web
import sys

if __name__ == '__main__':
    east_web = east_web()
    fun = sys.argv[1]

    if fun == 'help':
        east_web.dump(east_web.methods())
    else:
        do = getattr(east_web,'get_'+fun)
        do()