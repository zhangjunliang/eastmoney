import importlib
import sys

obj_name = sys.argv[1]
obj_fun = sys.argv[2]

obj = importlib.import_module('crontab.{}'.format(obj_name))
fun = getattr(obj.init(),obj_fun)
fun()