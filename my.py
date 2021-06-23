import time
from lib.east import east
from apscheduler.schedulers.background import BackgroundScheduler

if __name__ == '__main__':
    east = east()
    code_list = ['0.000001','1.601318','1.600519','0.300727','0.300353','0.300862']
    east.my(code_list)

    job_defaults = {
        'coalesce': True,  # 某个任务会积攒了好几次没执行如 5 次，下次这个作业被提交给执行器时，执行 5 次。设置 coalesce=True 后，只会执行一次。
        'max_instances': 1,  # 到达执行时间时，可同时执行的数量
        'misfire_grace_time': 2  # 当任务执行时间与设定时间差值的可接受范围，超过就不执行
    }
    schedule = BackgroundScheduler(job_defaults=job_defaults)
    schedule.add_job(getattr(east,'my'), 'interval',seconds=30, id='one',args=[code_list])
    schedule.start()
    while True:
        time.sleep(1)