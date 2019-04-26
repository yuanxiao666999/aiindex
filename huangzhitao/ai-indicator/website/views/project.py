# -*- coding:utf-8 -*-
# @Time :2019/4/18 9:17
__author__ = "HuangZhiTao"


import json
from flask import request
from . import views
from website.model import Session, Project, Project2Engineering
from utils.read_docx import read_docx


@views.route("/project/upload", methods=["POST"])
def project_upload():
    """项目文件上传"""

    data = {
        "code": 1,
    }

    # 获取上传文件对象
    file = request.files.get("file")
    file_name = file.filename
    file_type = file_name.split(".")[-1]

    # 判断文件的类型
    if file_type not in ("docx", "xlsx"):
        data["msg"] = "上传文件格式必须为docx、xlsx"

    project_name = request.form.get("project_name")
    if not project_name:
        return json.dumps(data)

    # 创建项目对象
    # project_obj = Project(**request.form)

    # 创建数据库链接会话
    sql_session = Session()

    # 添加项目
    # sql_session.add(project_obj)

    # 对docx文件进行操作
    if file_type == "docx":
        table_data = read_docx(file)
        if table_data:
            for k in table_data.keys():
                obj = Project2Engineering(project_name=project_name, engineering_name=k)
                sql_session.add(obj)
            else:
                try:
                    sql_session.commit()
                    data["code"] = 0
                except:
                    sql_session.rollback()
                    data["msg"] = "项目表格重复！！！"
                sql_session.close()

    return json.dumps(data)


@views.route("/project/tables", methods=["POST"])
def project_tables():

    # 获取项目名称
    project_name = request.form.get("project_name")

    # 创建数据库链接会话
    sql_session = Session()

    engineerings = sql_session.query(Project2Engineering.engineering_name).filter_by(project_name=project_name).all()
    data = {
        "code": 0,
    }
    if engineerings:
        data["data"] = [{"project_name": i[0]} for i in engineerings]
    else:
        data["code"] = 1
        data["msg"] = "项目不存在"
    sql_session.close()

    return json.dumps(data)
