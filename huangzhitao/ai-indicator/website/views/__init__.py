# -*- coding:utf-8 -*-
# @Time :2019/4/18 9:17
__author__ = "HuangZhiTao"


from flask import Blueprint


accout = Blueprint(
    "accout",
    __name__,
    template_folder="templates",
    # static_folder="static"
)


from . import account
