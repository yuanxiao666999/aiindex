# -*- coding:utf-8 -*-
# @Time :2019/4/26 13:00
__author__ = "HuangZhiTao"

# import os
from docx import Document
from website import model


def read_docx(file_path):

    data = dict()

    # 工程概况表
    gcgk_flag = False
    gcgk_append_flag = False

    # 工程特征表
    gctz_flag = False
    gctz_append_flag = False

    # 工程造价指标汇总
    zjzbhz_flag = False
    zjzbhz_append_flag = False

    # 分部分项工程造价指标
    fbfx_flag = False
    fbfx_flag_append_flag = False

    # 措施项目造价指标
    csxm_flag = False
    csxm_flag_append_flag = False

    # 其他项目造价指标
    qtxm_flag = False
    qtxm_flag_append_flag = False

    # 工程造价费用分析
    fyfx_flag = False
    fyfx_flag_append_flag = False

    # 主要消耗量指标
    xhzb_flag = False
    xhzb_flag_append_flag = False

    document = Document(file_path)
    tables = document.tables
    for table in tables:
        for row in table.rows:
            if not row.cells:
                continue
            # 表格每行内容
            li = [i.text for i in row.cells]

            # 判断是否是  工程概况表
            if "工程概况" in "".join(li[0].split()):
                gcgk_flag = True
                continue
            elif gcgk_flag and gcgk_append_flag is False:
                gcgk_append_flag = True
                data = {"工程概况": []}
                continue
            elif gcgk_append_flag and "".join(li[0].split()) == "价格取定期":
                data["工程概况"].append({
                    "engineering_name": "价格取定期",
                    "content": li[2].strip()
                })
                gcgk_flag = False
                gcgk_append_flag = False
                break
            elif gcgk_flag and gcgk_append_flag:
                if li[0] == li[1]:
                    temp_data = {
                        "engineering_name": li[0],
                    }
                else:
                    temp_data = {
                        "engineering_name": "-".join([li[0], li[1]]).strip(),
                    }
                temp_data["content"] = li[2].strip()
                data["工程概况"].append(temp_data)
                continue

            # 判断是否是  工程特征表
            if "工程特征" in "".join(li[0].split()):
                gctz_flag = True
                continue
            elif gctz_flag and gctz_append_flag is False:
                gctz_append_flag = True
                data["工程特征"] = []
                continue
            elif gctz_append_flag and "-".join([li[0], li[1]]) == "安装工程-其他工程":
                data["工程特征"].append({
                    "engineering_name": "安装工程-其他工程",
                    "desc": li[3].strip()
                })
                gctz_flag = False
                gctz_append_flag = False
                break
            elif gctz_flag and gctz_append_flag:
                if li[1] == li[2]:
                    temp_data = {
                        "engineering_name": "-".join([li[0], li[1]]).strip(),
                    }
                else:
                    temp_data = {
                        "engineering_name": "-".join([li[0], li[1], li[2]]).strip(),
                    }
                temp_data["desc"] = li[3].strip()
                data["工程特征"].append(temp_data)
                continue

            # 判断是否是  工程造价指标汇总表
            if "工程造价指标汇总" in "".join(li[0].split()):
                zjzbhz_flag = True
                continue
            elif zjzbhz_flag and zjzbhz_append_flag is False:
                zjzbhz_append_flag = True
                data["工程造价指标汇总"] = []
                continue
            elif zjzbhz_append_flag and li[0].strip() == "合计":
                data["工程造价指标汇总"].append({
                    "s_number": "合计",
                    "engineering_name": "合计",
                    "cost": li[2].strip(),
                    "square_cost": li[3].strip(),
                    "sum_prop": li[4].strip()
                })
                zjzbhz_flag = False
                zjzbhz_append_flag = False
                break
            elif zjzbhz_flag and zjzbhz_append_flag:
                if li[0].strip() == "序号":
                    continue
                data["工程造价指标汇总"].append({
                    "s_number": li[0].strip(),
                    "engineering_name": li[1].strip(),
                    "cost": li[2].strip(),
                    "square_cost": li[3].strip(),
                    "sum_prop": li[4].strip()
                })
                continue

            # 判断是否是  分部分项工程造价指标表
            if "分部分项工程造价指标" in "".join(li[0].split()):
                fbfx_flag = True
                continue
            elif fbfx_flag and fbfx_flag_append_flag is False:
                fbfx_flag_append_flag = True
                data["分部分项工程造价指标"] = []
                continue
            elif fbfx_flag_append_flag and li[0].strip() == "合计":
                data["分部分项工程造价指标"].append({
                    "s_number": "合计",
                    "engineering_name": "合计",
                    "cost": li[2].strip(),
                    "square_cost": li[3].strip(),
                    "sum_prop": li[4].strip()
                })
                fbfx_flag = False
                fbfx_flag_append_flag = False
                break
            elif fbfx_flag and fbfx_flag_append_flag:
                data["分部分项工程造价指标"].append({
                    "s_number": li[0].strip(),
                    "engineering_name": li[1].strip(),
                    "cost": li[2].strip(),
                    "square_cost": li[3].strip(),
                    "sum_prop": li[4].strip()
                })
                continue

            # 判断是否是  措施项目造价指标表
            if "措施项目造价指标" in "".join(li[0].split()):
                csxm_flag = True
                continue
            elif csxm_flag and csxm_flag_append_flag is False:
                csxm_flag_append_flag = True
                data["措施项目造价指标"] = []
                continue
            elif csxm_flag_append_flag and li[0].strip() == "合计":
                data["措施项目造价指标"].append({
                    "s_number": "合计",
                    "engineering_name": "合计",
                    "cost": li[2].strip(),
                    "square_cost": li[3].strip(),
                    "sum_prop": li[4].strip()
                })
                csxm_flag = False
                csxm_flag_append_flag = False
                break
            elif csxm_flag and csxm_flag_append_flag:
                data["措施项目造价指标"].append({
                    "s_number": li[0].strip(),
                    "engineering_name": li[1].strip(),
                    "cost": li[2].strip(),
                    "square_cost": li[3].strip(),
                    "sum_prop": li[4].strip()
                })
                continue

            # 判断是否是  其他项目造价指标表
            if "其他项目造价指标" in "".join(li[0].split()):
                qtxm_flag = True
                continue
            elif qtxm_flag and qtxm_flag_append_flag is False:
                qtxm_flag_append_flag = True
                data["其他项目造价指标"] = []
                continue
            elif qtxm_flag_append_flag and li[0].strip() == "合计":
                data["其他项目造价指标"].append({
                    "s_number": "合计",
                    "engineering_name": "合计",
                    "cost": li[2].strip(),
                    "square_cost": li[3].strip(),
                    "sum_prop": li[4].strip(),
                    "remarks": li[5].strip()
                })
                qtxm_flag = False
                qtxm_flag_append_flag = False
                break
            elif qtxm_flag and qtxm_flag_append_flag:
                data["其他项目造价指标"].append({
                    "s_number": li[0].strip(),
                    "engineering_name": li[1].strip(),
                    "cost": li[2].strip(),
                    "square_cost": li[3].strip(),
                    "sum_prop": li[4].strip(),
                    "remarks": li[5].strip()
                })
                continue

            # 判断是否是  工程造价费用分析表
            if "工程造价费用分析" in "".join(li[0].split()):
                fyfx_flag = True
                continue
            elif fyfx_flag and fyfx_flag_append_flag is False and li[4].strip() == "人工费":
                fyfx_flag_append_flag = True
                data["工程造价费用分析"] = []
                continue
            elif fyfx_flag_append_flag and li[0].strip() == "合计":
                data["工程造价费用分析"].append({
                    "s_number": "合计",
                    "engineering_name": "合计",
                    "cost": li[2].strip(),
                    "square_cost": li[3].strip(),
                    "artificial_prop": li[4].strip(),
                    "materials_prop": li[5].strip(),
                    "mechanics_prop": li[6].strip(),
                    "manage_prop": li[7].strip(),
                })
                fyfx_flag = False
                fyfx_flag_append_flag = False
                break
            elif fyfx_flag and fyfx_flag_append_flag:
                data["工程造价费用分析"].append({
                    "s_number": li[0].strip(),
                    "engineering_name": li[1].strip(),
                    "cost": li[2].strip(),
                    "square_cost": li[3].strip(),
                    "artificial_prop": li[4].strip(),
                    "materials_prop": li[5].strip(),
                    "mechanics_prop": li[6].strip(),
                    "manage_prop": li[7].strip(),
                })
                continue

            # 判断是否是  主要消耗量指标表
            if "主要消耗量指标" in "".join(li[0].split()):
                xhzb_flag = True
                continue
            elif xhzb_flag and xhzb_flag_append_flag is False:
                xhzb_flag_append_flag = True
                data["主要消耗量指标"] = []
                continue
            elif xhzb_flag_append_flag and li[0].strip().isdigit() is False:
                xhzb_flag = False
                xhzb_flag_append_flag = False
                break
            elif xhzb_flag and xhzb_flag_append_flag:
                if li[1] == li[2]:
                    temp_data = {"engineering_name": li[1].strip()}
                else:
                    temp_data = {"engineering_name": "-".join([li[1], li[2]]).strip()}
                temp_data["s_number"] = li[0].strip()
                temp_data["unit"] = li[3].strip()
                temp_data["consumption"] = li[4].strip()
                temp_data["square_consumption"] = li[5].strip()
                data["主要消耗量指标"].append(temp_data)
                continue

    return data


def docx_class_table(eng_name):
    if eng_name == "工程概况":
        table_class = model.EngineeringSurvey
        field = "engineeringSurvey"
    elif eng_name == "工程特征":
        table_class = model.EngineeringFeatures
        field = "engineeringFeatures"
    elif eng_name == "工程造价指标汇总":
        table_class = model.EngineeringZJHZ
        field = "engineeringZJHZ"
    elif eng_name == "分部分项工程造价指标":
        table_class = model.EngineeringFBFX
        field = "engineeringFBFX"
    elif eng_name == "措施项目造价指标":
        table_class = model.EngineeringCSXM
        field = "engineeringCSXM"
    elif eng_name == "其他项目造价指标":
        table_class = model.EngineeringQTXM
        field = "engineeringQTXM"
    elif eng_name == "工程造价费用分析":
        table_class = model.EngineeringFYFX
        field = "engineeringFYFX"
    elif eng_name == "主要消耗量指标":
        table_class = model.EngineeringXHL
        field = "engineeringXHL"
    else:
        table_class = None
        field = None

    return table_class, field
