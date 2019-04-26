# -*- coding:utf-8 -*-
# @Time :2019/4/18 9:17
__author__ = "HuangZhiTao"


import json
from flask import request
from . import views
from website.model import Session, Account, Project2Engineering
from utils.read_docx import read_docx


# @views.route("/project/select", methods=["GET", "POST"])
# def project_select():
#     """获取用户信息"""
#     # response数据格式
#     data = {
#         "code": 0,
#         "data": [],
#     }
#     # 创建数据库链接会话
#     sql_session = Session()
#
#     if request.method == "GET":
#         current_page = request.args.get("page")
#         limit = request.args.get("limit")
#
#         # 判断current_page、limit参数格式是否正确
#         if not (current_page and limit) or not (current_page.isdigit() and limit.isdigit()):
#             data["code"] = 1
#             data["msg"] = "请求数据错误"
#             return json.dumps(data)
#
#         current_page = int(current_page)
#         limit = int(limit)
#         start_num = (current_page-1)*limit
#
#         # 获取数据量
#         count = sql_session.query(func.count(Account.id)).first()
#         if not count:
#             data["code"] = 0
#             data["msg"] = "用户信息为空"
#             return json.dumps(data)
#
#         count = count[0]
#         if start_num > count:
#             start_num = (count // limit)*limit
#
#         # 获取当前页的数据
#         current_page_data = sql_session.query(Account.user, Account.passwd, ).filter(Account.permission != 0).offset(start_num).limit(limit).all()
#         data["count"] = count - 1
#         # #构造返回数据
#         for user, passwd in current_page_data:
#             data["data"].append({
#                 "user": user,
#                 "passwd": passwd
#             })
#         sql_session.close()
#
#     elif request.method == "POST":
#
#         # 获取查询用户名关键字
#         keyword = request.form.get("keyword")
#
#         user_data = sql_session.query(Account.id, Account.user, Account.passwd, Account.permission,).filter(Account.user.like(f"%{keyword}%")).all()
#         if user_data:
#             for i in user_data:
#                 data["data"].append({
#                     "id": i[0],
#                     "user": i[1],
#                     "passwd": i[2],
#                     "permission": i[3]
#                 })
#         else:
#             data["code"] = 1
#             data["msg"] = "用户不存在"
#
#     return json.dumps(data)
#
#
# @views.route("/project/insert", methods=["POST"])
# def project_insert():
#     """增加用户账号"""
#
#     data = {
#         "code": 0,
#         "data": []
#     }
#
#     user = request.form.get("user")
#     passwd = request.form.get("passwd")
#     permission = request.form.get("permission")
#
#     sql_session = Session()
#
#     # 去重用户名
#     dup_user = sql_session.query(Account.user).filter_by(user=user).all()
#     if dup_user:
#         data["code"] = 1
#     else:
#         user_obj = Account(user=user, passwd=passwd, permission=permission)
#         sql_session.add(user_obj)
#         sql_session.commit()
#     sql_session.close()
#
#     return json.dumps(data)
#
#
# @views.route("/project/delete", methods=["POST"])
# def project_delete():
#     """删除用户账号"""
#
#     data = {"code": 0}
#
#     user = request.form.get("user")
#     passwd = request.form.get("passwd")
#
#     sql_session = Session()
#     user_obj = sql_session.query(Account).filter_by(user=user, passwd=passwd)
#
#     if user_obj.all():
#         user_obj.delete()
#         sql_session.commit()
#     else:
#         data["code"] = 1
#     sql_session.close()
#
#     return json.dumps(data)


@views.route("/project/upload", methods=["POST"])
def project_upload():
    """项目文件上传"""

    data = {
        "code": 1,
    }
    # 获取项目名称
    project_name = request.form.get("project_name")

    # 获取上传文件对象
    file = request.files.get("file")
    file_name = file.filename
    file_type = file_name.split(".")[-1]

    # 判断文件的类型
    if file_type not in ("docx", "xlsx"):
        data["msg"] = "上传文件格式必须为docx、xlsx"

    # 对docx文件进行操作
    if file_type == "docx":
        table_data = read_docx(file)
        if table_data:
            # 创建数据库链接会话
            sql_session = Session()
            for k in table_data.keys():
                obj = Project2Engineering(project_name=project_name, engineering_name=k)
                sql_session.add(obj)
            else:
                data["code"] = 0
                sql_session.commit()
                sql_session.close()

    return json.dumps(data)
