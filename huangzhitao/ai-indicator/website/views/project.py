# -*- coding:utf-8 -*-
# @Time :2019/4/18 9:17
__author__ = "HuangZhiTao"


import json
from flask import request
from sqlalchemy import func, and_
from . import views
from website.model import *
from utils.read_docx import read_docx, docx_class_table


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
    project_obj = sql_session.query(Project).filter_by(project_name=project_name).first()

    # 不存在则创建项目，存在则更新项目
    if not project_obj:
        # 创建项目对象
        project_obj = Project(**request.form)

        # 添加项目
        sql_session.add(project_obj)
    else:
        sql_session.query(Project).filter_by(project_name=project_name).update(request.form)

    # 对docx文件进行操作
    if file_type == "docx":
        # 解析docx文件，返回数据
        table_data = read_docx(file)
        if table_data:
            # 项目对象
            project_ = sql_session.query(Project).filter_by(project_name=project_name).first()
            for k, v in table_data.items():
                # 判断项目对应的子项目对象是否存在
                obj = sql_session.query(Project2Engineering).filter_by(project_name=project_name, engineering_name=k).first()
                if obj:
                    data["msg"] = f"文件中存在已录入表:【{k}】"
                    return json.dumps(data)
                # 添加子项目对象
                obj = Project2Engineering(project_name=project_name, engineering_name=k)
                sql_session.add(obj)
                table_class, field = docx_class_table(k)
                # 添加子项目表数据对象
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
    """获取项目下的子项目名称"""
    data = {
        "code": 0,
        "data": []
    }
    # 获取项目名称
    project_name = request.args.get("project_name")
    if not project_name:
        data["code"] = 0
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


@views.route("/project/details")
def project_details():
    """返回所有的项目信息"""

    data = {
        "code": 0,
        "data": []
    }

    # 创建数据库链接会话
    sql_session = Session()

    # 获取数据量
    count = sql_session.query(func.count(Project.id)).first()
    if count:
        projects = sql_session.query(Project).all()
        for project in projects:
            data["data"].append({
                "project_name": project.project_name,
                "buildingType": project.buildingType,
                "buildingType2": project.buildingType2,
                "buildTime": project.buildTime,
                "buildingScale": project.buildingScale,
                "provider": project.provider,
                "provideTime": project.provideTime,
                "remarks": project.remarks,
            })
        else:
            data["count"] = count[0]
    else:
        data["code"] = 1
        data["msg"] = "已录入项目为空"

    sql_session.close()

    return json.dumps(data)


@views.route("/project/delete")
def project_delete():
    """项目信息的删除"""

    data = {
        "code": 1,
    }

    # 创建数据库链接会话
    sql_session = Session()

    project_name = request.args.get("project_name")
    if project_name:
        project = sql_session.query(Project).filter_by(project_name=project_name).first()
        if project:
            # 删除项目信息
            sql_session.query(Project).filter_by(project_name=project_name).delete()
            # 删除项目对应子表信息
            sql_session.query(Project2Engineering).filter_by(project_name=project_name).delete()
            sql_session.commit()
            data["code"] = 0
        else:
            data["msg"] = "项目不存在"
    sql_session.close()

    return json.dumps(data)


@views.route("/project/update")
def project_update():
    """项目信息的修改"""
    pass


@views.route("/project/table/delete")
def project_table_delete():
    """项目子表的删除"""
    data = {
        "code": 1
    }
    # 创建数据库链接会话
    sql_session = Session()

    # 项目子表对应model
    table_model = {
        "工程概况": EngineeringSurvey,
        "工程特征": EngineeringFeatures,
        "工程造价指标汇总": EngineeringZJHZ,
        "分部分项工程造价指标": EngineeringFBFX,
        "措施项目造价指标": EngineeringCSXM,
        "其他项目造价指标": EngineeringQTXM,
        "工程造价费用分析": EngineeringFYFX,
        "主要消耗量指标": EngineeringXHL
    }
    project_name = request.args.get("project_name")
    table_name = request.args.get("table_name")
    if project_name and table_name:
        # 查询项目和项目对应子表是否存在
        project_obj = sql_session.query(Project).filter_by(project_name=project_name).first()
        pro2eng = sql_session.query(Project2Engineering).filter(
            and_(Project2Engineering.project_name == project_name,
                 Project2Engineering.engineering_name == table_name
                 )).first()
        if project_obj and pro2eng:
            # 删除项目子表记录
            sql_session.query(table_model[table_name]).filter_by(project_id=project_obj.id).delete()
            # 删除项目对应子表记录
            sql_session.query(Project2Engineering).filter(
                and_(Project2Engineering.project_name == project_name,
                     Project2Engineering.engineering_name == table_name
                     )).delete()
            sql_session.commit()
            data["code"] = 0

    return json.dumps(data)


@views.route("/project/table/update")
def project_table_update():
    """项目子表信息的修改"""
    pass


@views.route("/project/table/details")
def project_table_details():
    """项目子表信息查找"""
    data = {
        "code": 1,
        "data": []
    }
    # 创建数据库链接会话
    sql_session = Session()

    # 项目子表对应model
    table_model = {
        "工程概况": EngineeringSurvey,
        "工程特征": EngineeringFeatures,
        "工程造价指标汇总": EngineeringZJHZ,
        "分部分项工程造价指标": EngineeringFBFX,
        "措施项目造价指标": EngineeringCSXM,
        "其他项目造价指标": EngineeringQTXM,
        "工程造价费用分析": EngineeringFYFX,
        "主要消耗量指标": EngineeringXHL
    }
    project_name = request.args.get("project_name")
    table_name = request.args.get("table_name")
    if project_name and table_name:
        # 查询项目和项目对应子表是否存在
        project_obj = sql_session.query(Project).filter_by(project_name=project_name).first()
        pro2eng = sql_session.query(Project2Engineering).filter(
            and_(Project2Engineering.project_name == project_name,
                 Project2Engineering.engineering_name == table_name
                 )).first()
        if project_obj and pro2eng:
            # 查询项目子表记录
            table_obj = sql_session.query(table_model[table_name]).filter_by(project_id=project_obj.id).all()
            for obj in table_obj:
                data["data"].append({
                    "engineering_name": obj.engineering_name,
                    "content": obj.content,
                })
                data["code"] = 0
    return json.dumps(data)
