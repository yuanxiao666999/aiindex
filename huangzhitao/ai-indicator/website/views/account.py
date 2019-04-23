# -*- coding:utf-8 -*-
# @Time :2019/4/18 9:17
__author__ = "HuangZhiTao"


import json
from flask import render_template, request, session, redirect
from . import accout
from utils.sql_connect import db
from settings import USER_INFO_TABLE


@accout.route("/home")
def home():
    # return render_template("/home/home.html")
    return "this home!!!"


@accout.route("/login", methods=["GET", "POST"])
def login():
    """用户登陆验证"""
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        user = request.form.get("user")
        passwd = request.form.get("passwd")
        sql_cmd = f"select permission from {USER_INFO_TABLE} where user=%s and passwd=%s"
        db.cur.execute(sql_cmd, (user, passwd))
        permission = db.cur.fetchone()
        if permission:
            session["user"] = user
            session["permission"] = permission[0]
            return redirect("/home")
        return json.dumps({"code": 1, "msg": "账户名或密码错误！！！"})
    return "request error"


@accout.route("/account/index/details")
def details():
    """获取所有用户信息"""
    # response数据格式
    data = {
        "code": "",
        "data": [],
    }

    current_page = request.args.get("page")
    limit = request.args.get("limit")

    # 判断current_page、limit参数格式是否正确
    if not (current_page and limit) or not (current_page.isdigit() and limit.isdigit()):
        data["code"] = 1
        data["msg"] = "请求数据错误"
        return json.dumps(data)

    # 获取当前页的数据
    sql_cmd = f"select user, passwd from {USER_INFO_TABLE} limit %s,%s "
    try:
        current_page = int(current_page)
        limit = int(limit)
        db.cur.execute(sql_cmd, ((current_page-1)*limit, limit))
    except:
        data["code"] = 1
        data["msg"] = "请求数据错误"
        return json.dumps(data)
    res = db.cur.fetchall()

    # 获取数据量
    sql_cmd = f"select count(id) from {USER_INFO_TABLE} "
    db.cur.execute(sql_cmd)
    data["count"] = db.cur.fetchone()[0]

    # 请求第一页的时候记录总记录数值
    # if current_page == 1:
    #     global count
    #     sql_cmd = "select count(id) from user_info "
    #     db.cur.execute(sql_cmd)
    #     count = db.cur.fetchone()[0]
    # else:
    #     count = count
    # 构造返回数据
    for user, passwd in res:
        data["data"].append({
            "user": user,
            "passwd": passwd
        })
    else:
        data["code"] = 0
    return json.dumps(data)


# @accout.route("/editAccount", methods=["GET", "POST"])
# def edit_account():
#     if request.method == "GET":
#         userid = request.args.get("userid")
#         sql_cmd = f"select username, passwd from {USER_INFO_TABLE} where id=%s"
#         db.cur.execute(sql_cmd, userid)
#         res = db.cur.fetchone()
#         data = {"username": res[0], "passwd": res[1], "userid": userid}
#         return render_template("/accout/editAccount.html", **data)
#     elif request.method == "POST":
#         userid = request.form.get("userid")
#         passwd = request.form.get("passwd")
#         sql_cmd = f"update {USER_INFO_TABLE} set passwd=%s where id=%s "
#         try:
#             db.cur.execute(sql_cmd, (passwd, userid))
#             return '1'
#         except:
#             return '0'
