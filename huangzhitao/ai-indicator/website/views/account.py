# -*- coding:utf-8 -*-
# @Time :2019/4/18 9:17
__author__ = "HuangZhiTao"


import json
from flask import render_template, request
from . import accout
from utils.sql_connect import db
from settings import USER_INFO_TABLE


# @accout.route("/home")
# def home():
#     return render_template("/home/home.html")
#
#
# @accout.route("/accout/console")
# def home_console():
#     return render_template("/accout/console.html")
#
#
# @accout.route("/accout/edit")
# def project_input():
#     return render_template("/accout/edit.html")


@accout.route("/account/")
def user_info():

    # response数据格式
    data = {
        "code": "",
        "data": [],
    }

    current_page = int(request.args.get("page"))
    limit = int(request.args.get("limit"))

    # 获取当前页的数据
    sql_cmd = f"select id, user, passwd from {USER_INFO_TABLE} limit %s,%s "
    try:
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

    for id_, user, passwd in res:
        data["data"].append({
            "userid": id_,
            "user": user,
            "passwd": passwd
        })
    else:
        data["code"] = 0
    return json.dumps(data)

#
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
