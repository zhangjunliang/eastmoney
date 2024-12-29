#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import importlib
import sys
import time
import argparse
import lib.public as public
from apscheduler.schedulers.background import BackgroundScheduler
import warnings

warnings.filterwarnings('ignore')


parser = argparse.ArgumentParser(description='run east')
parser.add_argument('-o', type=str, required=True, help='obj')
parser.add_argument('-f', type=str, required=True, default='', help='fun')
parser.add_argument('-p', default=None, help='params')
parser.add_argument('-t', default=0, help='jump')
parser.add_argument('-page', default=1, help='page')
parser.add_argument('-limit', default=10, help='limit')
parser.add_argument('-fields', default='id', help='fields')
parser.add_argument('-order', default='desc', help='order')

args = parser.parse_args()

public.init()
public.set('page',args.page)
public.set('limit',args.limit)
public.set('fields',args.fields)
public.set('order',args.order)

obj = importlib.import_module('crontab.{}'.format(args.o),args.o)

fun = getattr(obj.init(),args.f)

if args.p != None and args.p != '':
    fun(args.p)
else:
    fun()

args.t =int(args.t)

if args.t > 0:
    job_defaults = {
        'coalesce': True,  # 某个任务会积攒了好几次没执行如 5 次，下次这个作业被提交给执行器时，执行 5 次。设置 coalesce=True 后，只会执行一次。
        'max_instances': 1,  # 到达执行时间时，可同时执行的数量
        'misfire_grace_time': 2  # 当任务执行时间与设定时间差值的可接受范围，超过就不执行
    }
    schedule = BackgroundScheduler(job_defaults=job_defaults)
    job_args = []
    if args.p != None and args.p != '':
        job_args = [args.p]
    schedule.add_job(fun, 'interval', seconds=args.t, id='one', args=job_args)
    schedule.start()
    while True:
        time.sleep(1)