# -*- coding:utf-8 -*-
# @Time :2019/4/18 9:15
__author__ = "HuangZhiTao"


from flask import Flask
from .views import views


app = Flask(__name__)

app.config['SECRET_KEY'] = r'\xf1\x92Y\xdf\x8ejY\x04\x96\xb4V\x88\xfb\xfc\xb5\x18F\xa3\xee\xb9\xb9t\x01\xf0\x96'

app.register_blueprint(views)

