# -*- coding:utf-8 -*-
# @Time :2019/4/18 9:17
__author__ = "HuangZhiTao"


import json
from flask import request, session
from sqlalchemy import func
from . import accout
from website.model import Session, Users


@accout.route("/login", methods=["POST"])
def login():
    """用户登陆验证"""

    data = {
        "code": 0,
        "data": []
    }

    # 创建数据库链接会话
    sql_session = Session()
    # 获取用户信息
    user = request.form.get("user")
    passwd = request.form.get("passwd")
    # 数据库认证用户信息
    permission_ = sql_session.query(Users).filter_by(user=user, passwd=passwd).first()
    sql_session.close()
    if permission_:
        session["user"] = user
        session["permission"] = permission_.permission
        data["data"].append({"user": user, "permission": session["permission"]})
    else:
        data["code"] = 1

    return json.dumps(data)


@accout.route("/account/index/details", methods=["GET", "POST"])
def details():
    """获取用户信息"""
    # response数据格式
    data = {
        "code": 0,
        "data": [],
    }
    # 创建数据库链接会话
    sql_session = Session()

    if request.method == "GET":
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
        count = sql_session.query(func.count(Users.id)).first()[0]
        if start_num > count:
            start_num = (count // limit)*limit

        # 获取当前页的数据
        current_page_data = sql_session.query(Users.user, Users.passwd).offset(start_num).limit(limit).all()
        if not current_page_data:
            data["code"] = 1
        else:
            data["count"] = count
            # #构造返回数据
            for user, passwd in current_page_data:
                data["data"].append({
                    "user": user,
                    "passwd": passwd
                })
            sql_session.close()

    elif request.method == "POST":

        # 获取查询用户名关键字
        keyword = request.form.get("keyword")

        user_data = sql_session.query(Users.id, Users.user, Users.passwd, Users.permission,).filter(Users.user.like(f"%{keyword}%")).all()
        if user_data:
            for i in user_data:
                data["data"].append({
                    "id": i[0],
                    "user": i[1],
                    "passwd": i[2],
                    "permission": i[3]
                })
        else:
            data["code"] = 1

    return json.dumps(data)


@accout.route("/account/insert", methods=["POST"])
def accout_insert():
    """增加用户账号"""

    data = {
        "code": 0,
        "data": []
    }

    user = request.form.get("user")
    passwd = request.form.get("passwd")
    permission = request.form.get("permission")

    sql_session = Session()

    # 去重用户名
    dup_user = sql_session.query(Users.user).filter_by(user=user).all()
    if dup_user:
        data["code"] = 1
    else:
        user_obj = Users(user=user, passwd=passwd, permission=permission)
        sql_session.add(user_obj)
        sql_session.commit()
    sql_session.close()

    return json.dumps(data)


@accout.route("/account/delete", methods=["POST"])
def accout_delete():
    """删除用户账号"""

    data = {"code": 0}

    user = request.form.get("user")
    passwd = request.form.get("passwd")

    sql_session = Session()
    user_obj = sql_session.query(Users).filter_by(user=user, passwd=passwd)

    if user_obj.all():
        user_obj.delete()
        sql_session.commit()
    else:
        data["code"] = 1
    sql_session.close()

    return json.dumps(data)


@accout.route("/account/update", methods=["GET", "POST"])
def account_update():
    """用户信息更改"""

    data = {
        "code": 0,
        "data": [],
    }

    # 创建数据库链接会话
    sql_session = Session()

    if request.method == "GET":
        user = request.args.get("user")
        user_obj = sql_session.query(Users).filter_by(user=user).first()
        if user_obj:
            data["data"].append({"user": user, "passwd": user_obj.passwd}),

    elif request.method == "POST":
        user = request.form.get("user")
        passwd = request.form.get("passwd")
        user_obj = sql_session.query(Users).filter_by(user=user).first()
        if user_obj:
            sql_session.query(Users).filter_by(user=user).update({Users.passwd: passwd})
            sql_session.commit()
        else:
            data["code"] = 1
    else:
        data["code"] = 1

    # 关闭数据库链接会话
    sql_session.close()

    return json.dumps(data)
