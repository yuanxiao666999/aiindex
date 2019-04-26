# -*- coding:utf-8 -*-
# @Time :2019/4/18 9:17
__author__ = "HuangZhiTao"


import json
from flask import request
from . import views
from website.model import Session, Account, Project2Engineering
from utils.read_docx import read_docx


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
