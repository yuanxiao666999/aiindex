# -*- coding:utf-8 -*-
# @Time :2019/4/24 15:12
__author__ = "HuangZhiTao"


from sqlalchemy import create_engine, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()


class Account(Base):
    """用户信息表"""
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    user = Column(String(32), index=True, nullable=False)
    passwd = Column(String(32), nullable=False)
    permission = Column(Integer, nullable=False)


class Project(Base):
    """项目信息表"""
    __tablename__ = 'projects'

    pid = Column(Integer, primary_key=True)  # 项目ID
    project_name = Column(String(255), unique=True, nullable=False)  # 项目名称
    build_type = Column(String(100), nullable=False)  # 建筑类型
    build_date = Column(String(32), nullable=False)  # 建筑时间
    provider = Column(String(32), nullable=False)  # 提供者
    provider_date = Column(String(32), nullable=False)  # 提供时间
    remarks = Column(Text, nullable=False)  # 备注


class Project2Engineering(Base):
    """项目信息对应工程表"""
    __tablename__ = 'project2engineering'

    id = Column(Integer, primary_key=True)
    project_name = Column(String(255), index=True, nullable=False)  # 项目名称
    engineering_name = Column(String(255), index=True, nullable=False)  # 工程名称

    __table_args__ = (
        UniqueConstraint('project_name', 'engineering_name', name='uix_pro_eng'),
    )


class EngineeringSurvey(Base):
    """工程概况表"""
    __tablename__ = 'project_engineering_survey'

    id = Column(Integer, primary_key=True)
    project_name = Column(String(255), nullable=False)  # 父类项目
    engineering_name = Column(String(255), index=True, nullable=False)  # 工程名称
    content = Column(String(500), index=True, nullable=False)  # 内容


class EngineeringFeatures(Base):
    """工程特征表"""
    __tablename__ = 'project_engineering_features'

    id = Column(Integer, primary_key=True)
    project_name = Column(String(255), nullable=False)  # 父类项目
    engineering_name = Column(String(255), nullable=False)  # 工程名称
    desc = Column(String(500), index=True, nullable=False)  # 特征描述


class EngineeringZJHZ(Base):
    """工程造价指标汇总"""
    __tablename__ = 'project_engineering_zjhz'

    id = Column(Integer, primary_key=True)
    project_name = Column(String(255), nullable=False)  # 父类项目
    s_number = Column(Integer, nullable=False)  # 序号
    engineering_name = Column(String(255), nullable=False)  # 工程名称
    cost = Column(String(100), nullable=False)  # 造价（万元）
    square_cost = Column(String(100), nullable=False)  # 平方米造价（元/m2）
    sum_prop = Column(String(100), nullable=False)  # 占总造价比例（%）


class EngineeringFBFX(Base):
    """分部分项工程造价指标"""
    __tablename__ = 'project_engineering_fbfx'

    id = Column(Integer, primary_key=True)
    project_name = Column(String(255), nullable=False)  # 父类项目
    s_number = Column(Integer, nullable=False)  # 序号
    engineering_name = Column(String(255), nullable=False)  # 工程名称
    cost = Column(String(100), nullable=False)  # 造价（万元）
    square_cost = Column(String(100), nullable=False)  # 平方米造价（元/m2）
    sum_prop = Column(String(100), nullable=False)  # 占总造价比例（%）


class EngineeringCSXM(Base):
    """措施项目造价指标"""
    __tablename__ = 'project_engineering_csxm'

    id = Column(Integer, primary_key=True)
    project_name = Column(String(255), nullable=False)  # 父类项目
    s_number = Column(Integer, nullable=False)  # 序号
    engineering_name = Column(String(255), nullable=False)  # 工程名称
    cost = Column(String(100), nullable=False)  # 造价（万元）
    square_cost = Column(String(100), nullable=False)  # 平方米造价（元/m2）
    sum_prop = Column(String(100), nullable=False)  # 占总造价比例（%）


engine = create_engine(
    "mysql+pymysql://root:root@192.168.1.10:3306/aiindex?charset=utf8",
    max_overflow=0,  # 超过连接池大小外最多创建的连接
    pool_size=5,  # 连接池大小
    pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
)

Session = sessionmaker(bind=engine)
