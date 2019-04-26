# -*- coding:utf-8 -*-
# @Time :2019/4/26 13:00
__author__ = "HuangZhiTao"

# import os
from docx import Document


def read_docx(file_path):

    # if os.path.splitext(file_path)[-1] != ".docx":
    #     return

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
                data = {"工程概况": {"项目名称": [], "内容": []}}
                continue
            elif gcgk_append_flag and "".join(li[0].split()) == "价格取定期":
                data["工程概况"]["项目名称"].append("价格取定期")
                data["工程概况"]["内容"].append(li[2].strip())
                gcgk_flag = False
                gcgk_append_flag = False
                break
            elif gcgk_flag and gcgk_append_flag:
                if li[0] == li[1]:
                    data["工程概况"]["项目名称"].append(li[0])
                else:
                    data["工程概况"]["项目名称"].append("-".join([li[0], li[1]]).strip())
                data["工程概况"]["内容"].append(li[2].strip())
                continue

            # 判断是否是  工程特征表
            if "工程特征" in "".join(li[0].split()):
                gctz_flag = True
                continue
            elif gctz_flag and gctz_append_flag is False:
                gctz_append_flag = True
                data["工程特征"] = {"项目名称": [], "特征描述": []}
                continue
            elif gctz_append_flag and "-".join([li[0], li[1]]) == "安装工程-其他工程":
                data["工程特征"]["项目名称"].append("安装工程-其他工程")
                data["工程特征"]["特征描述"].append(li[3].strip())
                gctz_flag = False
                gctz_append_flag = False
                break
            elif gctz_flag and gctz_append_flag:
                if li[1] == li[2]:
                    data["工程特征"]["项目名称"].append("-".join([li[0], li[1]]).strip())
                else:
                    data["工程特征"]["项目名称"].append("-".join([li[0], li[1], li[2]]).strip())
                data["工程特征"]["特征描述"].append(li[3].strip())
                continue

            # 判断是否是  工程造价指标汇总表
            if "工程造价指标汇总" in "".join(li[0].split()):
                zjzbhz_flag = True
                continue
            elif zjzbhz_flag and zjzbhz_append_flag is False:
                zjzbhz_append_flag = True
                data["工程造价指标汇总"] = {
                    "序号": [], "项目名称": [], "造价(万元)": [],
                    "平方米造价（元/m2）": [], "占总造价比例（%）": []}
                continue
            elif zjzbhz_append_flag and li[0].strip() == "合计":
                data["工程造价指标汇总"]["序号"].append("合计")
                data["工程造价指标汇总"]["项目名称"].append("合计")
                data["工程造价指标汇总"]["造价(万元)"].append(li[2].strip())
                data["工程造价指标汇总"]["平方米造价（元/m2）"].append(li[3].strip())
                data["工程造价指标汇总"]["占总造价比例（%）"].append(li[4].strip())
                zjzbhz_flag = False
                zjzbhz_append_flag = False
                break
            elif zjzbhz_flag and zjzbhz_append_flag:
                if li[0].strip() == "序号":
                    continue
                data["工程造价指标汇总"]["序号"].append(li[0].strip())
                data["工程造价指标汇总"]["项目名称"].append(li[1].strip())
                data["工程造价指标汇总"]["造价(万元)"].append(li[2].strip())
                data["工程造价指标汇总"]["平方米造价（元/m2）"].append(li[3].strip())
                data["工程造价指标汇总"]["占总造价比例（%）"].append(li[4].strip())
                continue

            # 判断是否是  分部分项工程造价指标表
            if "分部分项工程造价指标" in "".join(li[0].split()):
                fbfx_flag = True
                continue
            elif fbfx_flag and fbfx_flag_append_flag is False:
                fbfx_flag_append_flag = True
                data["分部分项工程造价指标"] = {
                    "序号": [], "项目名称": [], "造价(万元)": [],
                    "平方米造价（元/m2）": [], "占总造价比例（%）": []}
                continue
            elif fbfx_flag_append_flag and li[0].strip() == "合计":
                data["分部分项工程造价指标"]["序号"].append("合计")
                data["分部分项工程造价指标"]["项目名称"].append("合计")
                data["分部分项工程造价指标"]["造价(万元)"].append(li[2].strip())
                data["分部分项工程造价指标"]["平方米造价（元/m2）"].append(li[3].strip())
                data["分部分项工程造价指标"]["占总造价比例（%）"].append(li[4].strip())
                fbfx_flag = False
                fbfx_flag_append_flag = False
                break
            elif fbfx_flag and fbfx_flag_append_flag:
                data["分部分项工程造价指标"]["序号"].append(li[0].strip())
                data["分部分项工程造价指标"]["项目名称"].append(li[1].strip())
                data["分部分项工程造价指标"]["造价(万元)"].append(li[2].strip())
                data["分部分项工程造价指标"]["平方米造价（元/m2）"].append(li[3].strip())
                data["分部分项工程造价指标"]["占总造价比例（%）"].append(li[4].strip())
                continue

            # 判断是否是  措施项目造价指标表
            if "措施项目造价指标" in "".join(li[0].split()):
                csxm_flag = True
                continue
            elif csxm_flag and csxm_flag_append_flag is False:
                csxm_flag_append_flag = True
                data["措施项目造价指标"] = {
                    "序号": [], "项目名称": [], "造价(万元)": [],
                    "平方米造价（元/m2）": [], "占总造价比例（%）": []}
                continue
            elif csxm_flag_append_flag and li[0].strip() == "合计":
                data["措施项目造价指标"]["序号"].append("合计")
                data["措施项目造价指标"]["项目名称"].append("合计")
                data["措施项目造价指标"]["造价(万元)"].append(li[2].strip())
                data["措施项目造价指标"]["平方米造价（元/m2）"].append(li[3].strip())
                data["措施项目造价指标"]["占总造价比例（%）"].append(li[4].strip())
                csxm_flag = False
                csxm_flag_append_flag = False
                break
            elif csxm_flag and csxm_flag_append_flag:
                data["措施项目造价指标"]["序号"].append(li[0].strip())
                data["措施项目造价指标"]["项目名称"].append(li[1].strip())
                data["措施项目造价指标"]["造价(万元)"].append(li[2].strip())
                data["措施项目造价指标"]["平方米造价（元/m2）"].append(li[3].strip())
                data["措施项目造价指标"]["占总造价比例（%）"].append(li[4].strip())
                continue

            # 判断是否是  其他项目造价指标表
            if "其他项目造价指标" in "".join(li[0].split()):
                qtxm_flag = True
                continue
            elif qtxm_flag and qtxm_flag_append_flag is False:
                qtxm_flag_append_flag = True
                data["其他项目造价指标"] = {
                    "序号": [], "项目名称": [], "造价(万元)": [],
                    "平方米造价（元/m2）": [], "占总造价比例（%）": [],
                    "备注": []
                }
                continue
            elif qtxm_flag_append_flag and li[0].strip() == "合计":
                data["其他项目造价指标"]["序号"].append("合计")
                data["其他项目造价指标"]["项目名称"].append("合计")
                data["其他项目造价指标"]["造价(万元)"].append(li[2].strip())
                data["其他项目造价指标"]["平方米造价（元/m2）"].append(li[3].strip())
                data["其他项目造价指标"]["占总造价比例（%）"].append(li[4].strip())
                data["其他项目造价指标"]["备注"].append(li[5].strip())
                qtxm_flag = False
                qtxm_flag_append_flag = False
                break
            elif qtxm_flag and qtxm_flag_append_flag:
                data["其他项目造价指标"]["序号"].append(li[0].strip())
                data["其他项目造价指标"]["项目名称"].append(li[1].strip())
                data["其他项目造价指标"]["造价(万元)"].append(li[2].strip())
                data["其他项目造价指标"]["平方米造价（元/m2）"].append(li[3].strip())
                data["其他项目造价指标"]["占总造价比例（%）"].append(li[4].strip())
                data["其他项目造价指标"]["备注"].append(li[5].strip())
                continue

            # 判断是否是  工程造价费用分析表
            if "工程造价费用分析" in "".join(li[0].split()):
                fyfx_flag = True
                continue
            elif fyfx_flag and fyfx_flag_append_flag is False and li[4].strip() == "人工费":
                fyfx_flag_append_flag = True
                data["工程造价费用分析"] = {
                    "序号": [], "项目名称": [], "造价(万元)": [],
                    "平方米造价（元/m2）": [], "占总造价比例（%）-人工费": [],
                    "占总造价比例（%）-材料费": [], "占总造价比例（%）-机械费": [],
                    "占总造价比例（%）-管理费和利润": [],
                }
                continue
            elif fyfx_flag_append_flag and li[0].strip() == "合计":
                data["工程造价费用分析"]["序号"].append("合计")
                data["工程造价费用分析"]["项目名称"].append("合计")
                data["工程造价费用分析"]["造价(万元)"].append(li[2].strip())
                data["工程造价费用分析"]["平方米造价（元/m2）"].append(li[3].strip())
                data["工程造价费用分析"]["占总造价比例（%）-人工费"].append(li[4].strip())
                data["工程造价费用分析"]["占总造价比例（%）-材料费"].append(li[5].strip())
                data["工程造价费用分析"]["占总造价比例（%）-机械费"].append(li[6].strip())
                data["工程造价费用分析"]["占总造价比例（%）-管理费和利润"].append(li[7].strip())
                fyfx_flag = False
                fyfx_flag_append_flag = False
                break
            elif fyfx_flag and fyfx_flag_append_flag:
                data["工程造价费用分析"]["序号"].append(li[0].strip())
                data["工程造价费用分析"]["项目名称"].append(li[1].strip())
                data["工程造价费用分析"]["造价(万元)"].append(li[2].strip())
                data["工程造价费用分析"]["平方米造价（元/m2）"].append(li[3].strip())
                data["工程造价费用分析"]["占总造价比例（%）-人工费"].append(li[4].strip())
                data["工程造价费用分析"]["占总造价比例（%）-材料费"].append(li[5].strip())
                data["工程造价费用分析"]["占总造价比例（%）-机械费"].append(li[6].strip())
                data["工程造价费用分析"]["占总造价比例（%）-管理费和利润"].append(li[7].strip())
                continue

            # 判断是否是  主要消耗量指标表
            if "主要消耗量指标" in "".join(li[0].split()):
                xhzb_flag = True
                continue
            elif xhzb_flag and xhzb_flag_append_flag is False:
                xhzb_flag_append_flag = True
                data["主要消耗量指标"] = {
                    "序号": [], "项目名称": [], "单位": [],
                    "消耗量": [], "百平方米消耗量": [],
                }
                continue
            elif xhzb_flag_append_flag and li[0].strip().isdigit() is False:
                xhzb_flag = False
                xhzb_flag_append_flag = False
                break
            elif xhzb_flag and xhzb_flag_append_flag:
                if li[1] == li[2]:
                    data["主要消耗量指标"]["项目名称"].append(li[1].strip())
                else:
                    data["主要消耗量指标"]["项目名称"].append("-".join([li[1], li[2]]).strip())
                data["主要消耗量指标"]["序号"].append(li[0].strip())
                data["主要消耗量指标"]["单位"].append(li[3].strip())
                data["主要消耗量指标"]["消耗量"].append(li[4].strip())
                data["主要消耗量指标"]["百平方米消耗量"].append(li[5].strip())
                continue

    return data
