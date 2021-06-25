# -*- coding=UTF-8 -*-
from flask_script import Manager
from app import app

#python manager.py runserver -h 127.0.0.1 -p 8090

# 指定使用那个配置来创建flask对象
flask_app = app.create()

# 添加扩展对象
manager = Manager(flask_app)

if __name__ == '__main__':
    manager.run()