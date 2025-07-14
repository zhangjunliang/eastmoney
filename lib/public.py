#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import sys
import time
from decimal import Decimal
import datetime


def init():
    global global_dict
    global_dict = {}

def set(name, value):
    global_dict[name] = value


def get(name, defValue=None):
    try:
        return global_dict[name]
    except KeyError:
        return defValue


def format_params(params):
    # params_list = list(row.split(":") for row in str(params).split(","))
    param_args = dict()
    for row in list(row.split(":") for row in str(params).split(",")):
        param_args[row[0]] = row[1]
    # print(param_args)
    return param_args

def get_market_info(stock_code,stock_name = '',market = 0 ,price = None):

    weight = 0
    market_type = get_market_code(stock_code)


    if 'ST' in stock_name:
        weight = -1000
    elif market_type > 2:
        weight = -900
    elif price != None and float(price) > 50:
        weight = -800

    '''
        code = '835179.BJ'
        code = '300661.SZ'
        code = '600192.SH'
        code = '688130.SH'
    '''
    #0其他,1主板2创业3科创4北交所
    if market_type == 4:
        market_str = 'BJ'
    elif market_type == 3:
        market_str = 'SH'
    elif market_type == 2:
        market_str = 'SZ'
    else:
        if market == '0':
            market_str = 'SZ'
        else:
            market_str = 'SH'

    data = {
        'market' : market,
        'market_type' : market_type,
        'market_str': market_str,
        'weight': weight
    }

    return data

def get_market_code(stock_code):
    # 去除可能的前导零
    # 判断科创板
    if stock_code.startswith('68'):
        #return '科创板'
        return 3
    # 判断创业板
    elif stock_code.startswith('3'):
        # return '创业板'
        return 2
    # 判断北交所
    elif stock_code.startswith('8'):
        return 4
    # 如果都不是，则返回不属于上述板块
    else:
        return 1

def avg(data,num = 5,field = ''):
    try:
        result = round(sum([float(i[field]) for i in data[0:num]]) / len(data[0:num]), 2)
        if len(data[0:num]) < num:
            result = 0
    except:
        result = 0
    return result

def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))
    return time_stamp

def timestamp_to_date(timestamp, format_string="%Y-%m-%d %H:%M:%S"):
    return time.strftime(format_string, time.localtime(timestamp))


def calculate_diff_rate(price_5, price_10, price_20):
    max_price = max(price_5, price_10, price_20)
    min_price = min(price_5, price_10, price_20)
    average_price = (price_5 + price_10 + price_20) / 3

    if average_price == 0:
        return "0.0"  # 避免除以零

    diff_rate = ((max_price - min_price) / average_price) * 100
    return f"{diff_rate:.1f}"  # 返回字符串类型的格式化结果


from decimal import Decimal
from datetime import datetime


def calculate_nine_turns(data):
    """
    计算神奇九转序列

    参数:
    data: 股票历史数据列表，包含每个交易日的开盘价、收盘价等信息

    返回:
    九转序列
    """
    nine_turns = []
    current_trend = None  # 当前趋势（上涨、下跌）
    current_count = 0  # 当前趋势的计数

    for i in range(1, len(data)):
        # 计算今日与昨日股价的涨跌幅
        current_price = data[i]['price']
        previous_price = data[i - 1]['price']
        price_change = current_price - previous_price

        # 判断趋势
        if price_change > 0:
            current_trend = 'up'
        elif price_change < 0:
            current_trend = 'down'
        else:
            continue  # 如果价格没有变化，跳过

        # 判断趋势是否改变
        if current_trend != getattr(current_trend, 'previous_trend', None) and current_trend is not None:
            nine_turns.append({
                'date': data[i]['day_time'],
                'price': current_price,
                'trend': current_trend,
                'count': 1
            })
            current_count = 1
        else:
            if current_trend == 'up' and current_count < 9:
                current_count += 1
                nine_turns[-1]['count'] = current_count
            elif current_trend == 'down' and current_count < 9:
                current_count += 1
                nine_turns[-1]['count'] = current_count
            else:
                nine_turns.append({
                    'date': data[i]['day_time'],
                    'price': current_price,
                    'trend': current_trend,
                    'count': 1
                })
                current_count = 1

    return nine_turns


def calculate_magic_nine_turns(data):
    """
    计算神奇九转，结合三转和五转的判断

    参数:
    data: 股票历史数据列表

    返回:
    神奇九转序列
    """
    nine_turns = calculate_nine_turns(data)
    magic_nine_turns = []

    # 这里可以结合三转和五转的判断逻辑
    # 简单示例：只记录连续上涨或下跌9天的转折点
    for i in range(len(nine_turns)):
        if nine_turns[i]['count'] == 9:
            magic_nine_turns.append(nine_turns[i])

    return magic_nine_turns





