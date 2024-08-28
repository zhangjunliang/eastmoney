import os
import sys

task = {
    0: {
        'name': '退出'
    },
    1 : {
        'name' : '自选',
        'task' : 'python run.py -o=east -f=my'
    },
    2 : {
        'name' : '涨',
        'task' : 'python run.py -o=east -f=info -p=stock_top'
    },
    3 : {
        'name' : '跌',
        'task' : 'python run.py -o=east -f=info -p=stock_low'
    },
    4 : {
        'name' : '成交',
        'task' : 'python run.py -o=east -f=info -p=stock_money'
    },
    5 : {
        'name' : '换手',
        'task' : 'python run.py -o=east -f=info -p=stock_change'
    },
    6 : {
        'name' : '涨速',
        'task' : 'python run.py -o=east -f=info -p=tmp_top'
    },
    7 : {
        'name' : '跌速',
        'task' : 'python run.py -o=east -f=info -p=tmp_low'
    },
    8 : {
        'name' : '净流速',
        'task' : 'python run.py -o=east -f=info -p=tmp_top'
    },
    9 : {
        'name' : '净流入',
        'task' : 'python run.py -o=east -f=info -p=stock_input'
    },
    # 10 : { 没有写
    #     'name' : '净流速',
    #     'task' : 'python run.py -o=east -f=info -p=tmp_top'
    # },
    11 : {
        'name' : '量比',
        'task' : 'python run.py -o=east -f=info -p=stock_amount'
    },
    12 : {
        'name' : '盘口异动',
        'task' : 'python run.py -o=east -f=info -p=tmp_change'
    },
    13 : {
        'name' : '板块行业',
        'task' : 'python run.py -o=east -f=info -p=bk_industry'
    },
    14 : {
        'name' : '板块概念',
        'task' : 'python run.py -o=east -f=info -p=bk_concept'
    },
    15 : {
        'name' : '板块地区',
        'task' : 'python run.py -o=east -f=info -p=bk_area'
    },
    16 : {
        'name' : '板块涨速',
        'task' : 'python run.py -o=east -f=info -p=tmp_bk'
    },
    18 : {
        'name' : '板块流入',
        'task' : 'python run.py -o=east -f=info -p=bk_input'
    },
    19 : {
        'name' : '板块流出',
        'task' : 'python run.py -o=east -f=info -p=bk_out'
    },
    20 : {
        'name' : '可转债',
        'task' : 'python run.py -o=east -f=info -p=kzc_top'
    },
    21 : {
        'name' : '行情',
        'task' : 'python run.py -o=east -f=info -p=market'
    },
    22 : {
        'name' : '热门',
        'task' : 'python run.py -o=east -f=info -p=hot'
    },
    23 : {
        'name' : '行情',
        'task' : 'python run.py -o=east -f=info -p=market'
    },
    99 : {
        'name' : '任务-stock',
        'task' : 'task.bat'
    },
    100 : {
        'name' : '任务-bk',
        'task' : 'task_bk.bat'
    }
}

'''


板块涨速



'''

while True:  # 创建一个无限循环

    task_list = ['{}:{}'.format(k,task[k]['name']) for k in task]

    user_input = input(str(task_list) + "\n")
    try:
        if user_input.lower() == 'exit':  # 检查用户是否想要退出
            print("退出程序。")
            break  # 退出循环
        elif user_input.isdigit():  # 检查输入是否为数字
            number = int(user_input)  # 将输入转换为整数
            if number == 0:
                print(task[number]['name'])
                break
            else:
                os.system(task[number]['task'])
    except Exception as e:
        print("error:{}".format(e))


# 执行ls命令列出当前目录下的文件
# result = os.system('python run.py -o=east -f=my')
# print("命令执行完毕，返回值为：", result)