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
    user = Column(String(32), index=True, nullable=False, comment="用户名")
    passwd = Column(String(32), nullable=False, comment="用户密码")
    permission = Column(Integer, nullable=False, comment="用户权限")
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


# class EngineeringSurvey(Base):
#     """工程概况表"""
#     __tablename__ = 'project_engineering_survey'
#
#     id = Column(Integer, primary_key=True)
#     engineering_name = Column(String(500), index=True, nullable=False)  # 工程名称
#     content = Column(String(500), index=True, nullable=False)  # 内容
#     parent_project_id = Column(String(500), nullable=False)  # 父类项目I

#
# class EngineeringFeatures(Base):
#     """工程特征表"""
#     __tablename__ = 'project_engineering_features'
#
#     id = Column(Integer, primary_key=True)
#     engineering_name = Column(String(500), index=True, nullable=False)  # 项目名称
#     desc = Column(String(500), index=True, nullable=False)  # 特征描述
#     parent_project_id = Column(Integer, nullable=False)  # 父类项目ID

"""
class MyClass(Base):
    __tablename__ = 'mytable'
    id = Column(Integer, primary_key=True)
    children = relationship("MyOtherClass",
                            cascade="all, delete-orphan",
                            passive_deletes=True)
    children2 = relationship("MyOtherClass2",
                            cascade="all, delete-orphan",
                            passive_deletes=True)


class MyOtherClass(Base):
    __tablename__ = 'myothertable'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer,
                       ForeignKey('mytable.id', ondelete='CASCADE')
                       )


class MyOtherClass2(Base):
    __tablename__ = 'myothertable2'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer,
                       ForeignKey('mytable.id', ondelete='CASCADE')
                       )

"""

engine = create_engine(
    "mysql+pymysql://root:root@192.168.1.10:3306/aiindex?charset=utf8",
    max_overflow=0,  # 超过连接池大小外最多创建的连接
    pool_size=5,  # 连接池大小
    pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
)

#
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
#
#
# if __name__ == '__main__':
#     init_db()
#
#
#
