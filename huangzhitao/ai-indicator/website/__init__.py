# -*- coding:utf-8 -*-
# @Time :2019/4/18 9:15
__author__ = "HuangZhiTao"


from flask import Flask
from .views import accout


app = Flask(__name__)

app.register_blueprint(accout)
