# -*- coding=UTF-8 -*-
import redis
import os
import random
from itertools import product
import yaml
import io

f = io.open('config.yaml', 'r', encoding='utf-8')
config = yaml.load(stream=f.read(), Loader=yaml.FullLoader)


class Config(object):
    def __init__(self):
        self.mysql = {
            'host': config['mysql_host'],
            'port': config['mysql_port'],
            'user': config['mysql_user'],
            'password': config['mysql_password'],
            'database': config['mysql_database'],
            'charset': config['mysql_charset'],
            'timeout': config['mysql_timeout'],
        }

if __name__ == "__main__":
    Config()