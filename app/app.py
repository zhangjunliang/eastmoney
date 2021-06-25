#!/usr/bin/env python
# -*- coding=UTF-8 -*-

from flask import Flask
from flask_session import Session
from app.init import action as init_action

def create():
    # 创建flask对象
    app = Flask(__name__, static_folder="")

    # 加载配置
    # conf = config()
    # app.config.from_object(conf)

    Session(app)

    #注册
    app.register_blueprint(init_action)

    return app


if __name__ == "__main__":
    pass