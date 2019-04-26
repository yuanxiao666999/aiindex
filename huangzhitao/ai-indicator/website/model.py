# -*- coding:utf-8 -*-
# @Time :2019/4/24 15:12
__author__ = "HuangZhiTao"


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
# from settings import SQLALCHEMY_DATABASE_URI


Base = declarative_base()


class Users(Base):
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

    pid = Column(Integer, primary_key=True)
    project_name = Column(String(255), index=True, nullable=False)
    build_type = Column(String(100), nullable=False)
    build_date = Column(String(32), nullable=False)
    provider = Column(String(32), nullable=False)
    provider_date = Column(String(32), nullable=False)
    remarks = Column(Text, nullable=False)
    # sub_project = Column(String(255), nullable=False)


class EngineeringSurvey(Base):
    """工程概况表"""
    __tablename__ = 'project_engineering_survey'

    id = Column(Integer, primary_key=True)
    project_name = Column(String(500), index=True, nullable=False)
    content = Column(String(500), index=True, nullable=False)
    parent_project_id = Column(Integer, nullable=False)


class EngineeringFeatures(Base):
    """工程特征表"""
    __tablename__ = 'project_engineering_features'

    id = Column(Integer, primary_key=True)
    project_name = Column(String(500), index=True, nullable=False)
    desc = Column(String(500), index=True, nullable=False)
    parent_project_id = Column(Integer, nullable=False)


engine = create_engine(
    "mysql+pymysql://root:root@127.0.0.1:3306/aiindex?charset=utf8",
    max_overflow=0,  # 超过连接池大小外最多创建的连接
    pool_size=5,  # 连接池大小
    pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
)


Session = sessionmaker(bind=engine)


#
# def init_db():
#     """
#     根据类创建数据库表
#     :return:
#     """
#     engine = create_engine(
#         "mysql+pymysql://root:111@127.0.0.1:3306/ai?charset=utf8",
#         max_overflow=0,  # 超过连接池大小外最多创建的连接
#         pool_size=5,  # 连接池大小
#         pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
#         pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
#     )
#
#     Base.metadata.create_all(engine)


# if __name__ == '__main__':
    # init_db()



