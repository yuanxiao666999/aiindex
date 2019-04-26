# -*- coding:utf-8 -*-
# @Time :2019/4/24 15:12
__author__ = "HuangZhiTao"


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
# from settings import SQLALCHEMY_DATABASE_URI


Base = declarative_base()


class Account(Base):
    """用户信息表"""
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    user = Column(String(32), index=True, nullable=False)
    passwd = Column(String(32), nullable=False)
    permission = Column(Integer, nullable=False)
    # email = Column(String(32), unique=True)
    # ctime = Column(DateTime, default=datetime.datetime.now)
    # extra = Column(Text, nullable=True)

    __table_args__ = (
        # UniqueConstraint('id', 'name', name='uix_id_name'),
        # Index('ix_id_name', 'name', 'email'),
    )


class Project(Base):
    """项目信息表"""
    __tablename__ = 'projects'

    pid = Column(Integer, primary_key=True)  # 项目ID
    project_name = Column(String(255), index=True, nullable=False)  # 项目名称
    build_type = Column(String(100), nullable=False)  # 建筑类型
    build_date = Column(String(32), nullable=False)  # 建筑时间
    provider = Column(String(32), nullable=False)  # 提供者
    provider_date = Column(String(32), nullable=False)  # 提供时间
    remarks = Column(Text, nullable=False)  # 备注
    # sub_project = Column(String(255), nullable=False, comment="子类工程表名称")


class Project2Engineering(Base):
    """项目信息对应工程表"""
    __tablename__ = 'project2engineering'

    id = Column(Integer, primary_key=True)
    project_name = Column(String(500), index=True, nullable=False)  # 项目名称
    engineering_name = Column(String(500), index=True, nullable=False)  # 工程名称


engine = create_engine(
    "mysql+pymysql://root:root@192.168.1.10:3306/aiindex?charset=utf8",
    max_overflow=0,  # 超过连接池大小外最多创建的连接
    pool_size=5,  # 连接池大小
    pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
)

#
Session = sessionmaker(bind=engine)
