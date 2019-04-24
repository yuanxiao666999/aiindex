# -*- coding:utf-8 -*-
# @Time :2019/4/18 9:17
__author__ = "HuangZhiTao"


import json
from flask import render_template, request, session, redirect
from . import accout
from utils.sql_connect import db
from settings import USER_INFO_TABLE


@accout.route("/login", methods=["POST",])
def login():
    """用户登陆验证"""
    params = request.form.to_dict()
    user = params.get("user")
    passwd = params.get("passwd")
    sql_cmd = f"select permission from {USER_INFO_TABLE} where user=%s and passwd=%s"
    db.cur.execute(sql_cmd, (user, passwd))
    permission = db.cur.fetchone()
    if permission:
        session["user"] = user
        session["permission"] = permission[0]
        data = {
            "code": 0,
            "data": {
                "user": user,
                "permission": permission[0]
            },
        }
    else:
        data = {
            "code": 1,
            "msg": "账户名或密码错误！！！"
        }
    return json.dumps(data)


@accout.route("/account/index/details")
def details():
    """获取所有用户信息"""
    # response数据格式
    data = {
        "code": 0,
        "data": [],
    }
    current_page = request.args.get("page")
    limit = request.args.get("limit")

    # 判断current_page、limit参数格式是否正确
    if not (current_page and limit) or not (current_page.isdigit() and limit.isdigit()):
        data["code"] = 1
        data["msg"] = "请求数据错误"
        return json.dumps(data)

    current_page = int(current_page)
    limit = int(limit)
    start_num = (current_page-1)*limit

    # 获取数据量
    sql_cmd = f"select count(id) from {USER_INFO_TABLE} "
    db.cur.execute(sql_cmd)
    count = db.cur.fetchone()[0]
    if start_num > count:
        start_num = (count // limit)*limit

    # 获取当前页的数据
    sql_cmd = f"select user, passwd from {USER_INFO_TABLE} limit %s,%s "
    try:
        db.cur.execute(sql_cmd, (start_num, limit))
    except:
        data["code"] = 1
        data["msg"] = "请求数据错误"
        return json.dumps(data)
    res = db.cur.fetchall()
    data["count"] = count

    # 构造返回数据
    for user, passwd in res:
        data["data"].append({
            "user": user,
            "passwd": passwd
        })
    print(data)
    return json.dumps(data)


@accout.route("/account/update", methods=["GET", "POST"])
def account_update():
    if request.method == "GET":
        user = request.args.get("user")
        sql_cmd = f"select passwd from {USER_INFO_TABLE} where user=%s"
        db.cur.execute(sql_cmd, user)
        res = db.cur.fetchone()
        if res:
            data = {
                "code": 0,
                "data": [{"user": user, "passwd": res[0]}],
            }
            return json.dumps(data)
        return json.dumps({"code": 1, "msg": "请求错误"})

    elif request.method == "POST":
        user = request.form.get("user")
        passwd = request.form.get("passwd")
        sql_cmd = f"update {USER_INFO_TABLE} set passwd=%s where user=%s "
        try:
            db.cur.execute(sql_cmd, (passwd, user))
            return json.dumps({"code": 0, "msg": "修改成功"})
        except:
            json.dumps({"code": 1, "msg": "修改失败"})
