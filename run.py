import importlib
import sys
import time
from apscheduler.schedulers.background import BackgroundScheduler

obj_name = sys.argv[1]
obj_fun = sys.argv[2]
try:
    obj_params = sys.argv[3]
except Exception as e:
    obj_params = None

obj = importlib.import_module('crontab.{}'.format(obj_name))

fun = getattr(obj.init(),obj_fun)
if obj_params:
    fun(obj_params)
else:
    if obj_fun == 'my':
        code_list = ['0.000001', '1.601318', '1.600519', '0.300727', '0.300353', '0.300862']
        fun(code_list)
        job_defaults = {
            'coalesce': True,  # 某个任务会积攒了好几次没执行如 5 次，下次这个作业被提交给执行器时，执行 5 次。设置 coalesce=True 后，只会执行一次。
            'max_instances': 1,  # 到达执行时间时，可同时执行的数量
            'misfire_grace_time': 2  # 当任务执行时间与设定时间差值的可接受范围，超过就不执行
        }
        schedule = BackgroundScheduler(job_defaults=job_defaults)
        schedule.add_job(fun, 'interval', seconds=30, id='one', args=[code_list])
        schedule.start()
        while True:
            time.sleep(1)
    else:
        fun()
try:
    pass
except Exception as e:
    print(e)