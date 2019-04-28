# -*- coding:utf-8 -*-
# @Time :2019/4/18 9:17
__author__ = "HuangZhiTao"


import json
from flask import request
from . import views
from website.model import *
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

    # 创建数据库链接会话
    sql_session = Session()

    # 判断项目是否存在
    project_obj = sql_session.query(Project).filter_by(project_name=project_name).all()

    if not project_obj:
        # 创建项目对象
        project_obj = Project(**request.form)

        # 添加项目
        sql_session.add(project_obj)

    # 对docx文件进行操作
    if file_type == "docx":
        # 解析docx文件，返回数据
        table_data = read_docx(file)
        if table_data:
            # 项目对象
            project_ = sql_session.query(Project).filter_by(project_name=project_name).first()
            for k, v in table_data.items():
                # 项目对应的子项目对象
                obj = Project2Engineering(project_name=project_name, engineering_name=k)
                sql_session.add(obj)
                table_class = None
                field = None
                if k == "工程概况":
                    table_class = EngineeringSurvey
                    field = "engineeringSurvey"
                if k == "工程特征":
                    table_class = EngineeringFeatures
                    field = "engineeringFeatures"
                if k == "工程造价指标汇总":
                    table_class = EngineeringZJHZ
                    field = "engineeringZJHZ"
                if k == "分部分项工程造价指标":
                    table_class = EngineeringFBFX
                    field = "engineeringFBFX"
                if k == "措施项目造价指标":
                    table_class = EngineeringCSXM
                    field = "engineeringCSXM"
                if k == "其他项目造价指标":
                    table_class = EngineeringQTXM
                    field = "engineeringQTXM"
                if k == "工程造价费用分析":
                    table_class = EngineeringFYFX
                    field = "engineeringFYFX"
                if k == "主要消耗量指标":
                    table_class = EngineeringXHL
                    field = "engineeringXHL"

                if table_class:
                    for j in v:
                        if isinstance(j, dict):
                            getattr(project_, field).append(table_class(**j))
                    sql_session.add(project_)
            else:
                try:
                    sql_session.commit()
                    data["code"] = 0
                except:
                    sql_session.rollback()
                    data["msg"] = "项目表格重复！！！"
                sql_session.close()

    return json.dumps(data)


@views.route("/project/tables")
def project_tables():

    data = {
        "code": 0,
        "data": []
    }
    # 获取项目名称
    project_name = request.args.get("project_name")
    if not project_name:
        data["code"] = 1
        return json.dumps(data)

    # 创建数据库链接会话
    sql_session = Session()

    engineerings = sql_session.query(Project2Engineering.engineering_name).filter_by(project_name=project_name).all()

    if engineerings:
        for i in engineerings:
            data["data"].append({"engineering_name": i[0]})
    else:
        data["code"] = 1
        data["msg"] = "项目不存在"
    sql_session.close()

    return json.dumps(data)
