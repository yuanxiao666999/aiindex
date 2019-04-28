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
    user = Column(String(32), index=True, nullable=False, comment="用户名")
    passwd = Column(String(32), nullable=False, comment="用户密码")
    permission = Column(Integer, nullable=False, comment="用户权限")


class Project(Base):
    """项目信息表"""
    __tablename__ = 'projects'

    pid = Column(Integer, primary_key=True)  # 项目ID
    project_name = Column(String(255), unique=True, nullable=False)  # 项目名称
    build_type = Column(String(100))  # 建筑类型
    build_date = Column(String(32))  # 建筑时间
    provider = Column(String(32))  # 提供者
    provider_date = Column(String(32))  # 提供时间
    remarks = Column(Text)  # 备注
    engineeringSurvey = relationship("EngineeringSurvey", cascade="all, delete-orphan", passive_deletes=True)
    engineeringFeatures = relationship("EngineeringFeatures", cascade="all, delete-orphan", passive_deletes=True)
    engineeringZJHZ = relationship("EngineeringZJHZ", cascade="all, delete-orphan", passive_deletes=True)
    engineeringFBFX = relationship("EngineeringFBFX", cascade="all, delete-orphan", passive_deletes=True)
    engineeringCSXM = relationship("EngineeringCSXM", cascade="all, delete-orphan", passive_deletes=True)
    engineeringQTXM = relationship("EngineeringQTXM", cascade="all, delete-orphan", passive_deletes=True)
    engineeringFYFX = relationship("EngineeringFYFX", cascade="all, delete-orphan", passive_deletes=True)
    engineeringXHL = relationship("EngineeringXHL", cascade="all, delete-orphan", passive_deletes=True)


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
    # project_name = Column(String(255))  # 父类项目
    engineering_name = Column(String(255), index=True)  # 工程名称
    content = Column(String(500), index=True)  # 内容
    project_id = Column(Integer, ForeignKey('projects.pid', ondelete='CASCADE'))


class EngineeringFeatures(Base):
    """工程特征表"""
    __tablename__ = 'project_engineering_features'

    id = Column(Integer, primary_key=True)
    # project_name = Column(String(255))  # 父类项目
    engineering_name = Column(String(255))  # 工程名称
    desc = Column(String(500), index=True)  # 特征描述
    project_id = Column(Integer, ForeignKey('projects.pid', ondelete='CASCADE'))


class EngineeringZJHZ(Base):
    """工程造价指标汇总"""
    __tablename__ = 'project_engineering_zjhz'

    id = Column(Integer, primary_key=True)
    # project_name = Column(String(255))  # 父类项目
    s_number = Column(Integer)  # 序号
    engineering_name = Column(String(255))  # 工程名称
    cost = Column(String(100))  # 造价（万元）
    square_cost = Column(String(100))  # 平方米造价（元/m2）
    sum_prop = Column(String(100), nullable=False)  # 占总造价比例（%）
    project_id = Column(Integer, ForeignKey('projects.pid', ondelete='CASCADE'))


class EngineeringFBFX(Base):
    """分部分项工程造价指标"""
    __tablename__ = 'project_engineering_fbfx'

    id = Column(Integer, primary_key=True)
    # project_name = Column(String(255))  # 父类项目
    s_number = Column(Integer)  # 序号
    engineering_name = Column(String(255))  # 工程名称
    cost = Column(String(100))  # 造价（万元）
    square_cost = Column(String(100))  # 平方米造价（元/m2）
    sum_prop = Column(String(100))  # 占总造价比例（%）
    project_id = Column(Integer, ForeignKey('projects.pid', ondelete='CASCADE'))


class EngineeringCSXM(Base):
    """措施项目造价指标"""
    __tablename__ = 'project_engineering_csxm'

    id = Column(Integer, primary_key=True)
    # project_name = Column(String(255))  # 父类项目
    s_number = Column(Integer)  # 序号
    engineering_name = Column(String(255))  # 工程名称
    cost = Column(String(100))  # 造价（万元）
    square_cost = Column(String(100))  # 平方米造价（元/m2）
    sum_prop = Column(String(100))  # 占总造价比例（%）
    project_id = Column(Integer, ForeignKey('projects.pid', ondelete='CASCADE'))


class EngineeringQTXM(Base):
    """其他项目造价指标"""
    __tablename__ = 'project_engineering_qtxm'

    id = Column(Integer, primary_key=True)
    # project_name = Column(String(255))  # 父类项目
    s_number = Column(Integer)  # 序号
    engineering_name = Column(String(255))  # 工程名称
    cost = Column(String(100))  # 造价（万元）
    square_cost = Column(String(100))  # 平方米造价（元/m2）
    sum_prop = Column(String(100))  # 占总造价比例（%）
    remarks = Column(String(100))  # 备注
    project_id = Column(Integer, ForeignKey('projects.pid', ondelete='CASCADE'))


class EngineeringFYFX(Base):
    """工程造价费用分析"""
    __tablename__ = 'project_engineering_fyfx'

    id = Column(Integer, primary_key=True)
    # project_name = Column(String(255))  # 父类项目
    s_number = Column(Integer)  # 序号
    engineering_name = Column(String(255))  # 工程名称
    cost = Column(String(100))  # 造价（万元）
    square_cost = Column(String(100))  # 平方米造价（元/m2）
    artificial_prop = Column(String(100))  # 占总造价比例（%） 人工费
    materials_prop = Column(String(100))  # 占总造价比例（%） 材料费
    mechanics_prop = Column(String(100))  # 占总造价比例（%） 机械费
    manage_prop = Column(String(100))  # 占总造价比例（%） 管理费和利润
    project_id = Column(Integer, ForeignKey('projects.pid', ondelete='CASCADE'))


class EngineeringXHL(Base):
    """主要消耗量指标"""
    __tablename__ = 'project_engineering_xhl'

    id = Column(Integer, primary_key=True)
    # project_name = Column(String(255))  # 父类项目
    s_number = Column(Integer)  # 序号
    engineering_name = Column(String(255))  # 工程名称
    unit = Column(String(100))  # 单位
    consumption = Column(String(100))  # 消耗量
    square_consumption = Column(String(100))  # 百平方米消耗量
    project_id = Column(Integer, ForeignKey('projects.pid', ondelete='CASCADE'))


engine = create_engine(
    "mysql+pymysql://root:root@192.168.1.10:3306/aiindex?charset=utf8",
    max_overflow=0,  # 超过连接池大小外最多创建的连接
    pool_size=5,  # 连接池大小
    pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
)

Session = sessionmaker(bind=engine)
