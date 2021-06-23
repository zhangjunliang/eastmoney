import importlib
import sys
import time
import argparse
from apscheduler.schedulers.background import BackgroundScheduler

parser = argparse.ArgumentParser(description='run east')
parser.add_argument('-o', type=str, required=True, help='obj')
parser.add_argument('-f', type=str, required=True, default='', help='fun')
parser.add_argument('-p', default=None, help='params')
parser.add_argument('-t', type=int, default=0, help='params')

args = parser.parse_args()

obj = importlib.import_module('crontab.{}'.format(args.o))

fun = getattr(obj.init(),args.f)

if args.f == 'my':
    args.p = ['0.000001', '1.601318', '1.600519', '0.300727', '0.300353', '0.300862']
print(args)

if args.p != None:
    fun(args.p)
else:
    fun()

if args.t > 0:
    job_defaults = {
        'coalesce': True,  # 某个任务会积攒了好几次没执行如 5 次，下次这个作业被提交给执行器时，执行 5 次。设置 coalesce=True 后，只会执行一次。
        'max_instances': 1,  # 到达执行时间时，可同时执行的数量
        'misfire_grace_time': 2  # 当任务执行时间与设定时间差值的可接受范围，超过就不执行
    }
    schedule = BackgroundScheduler(job_defaults=job_defaults)
    schedule.add_job(fun, 'interval', seconds=args.t, id='one', args=[args.p])
    schedule.start()
    while True:
        time.sleep(1)