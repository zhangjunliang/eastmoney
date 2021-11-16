#!/usr/bin/env python
# -*- coding=UTF-8 -*-


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
