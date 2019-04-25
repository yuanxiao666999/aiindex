# -*- coding:utf-8 -*-
# @Time :2019/4/24 15:12
__author__ = "HuangZhiTao"


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Users(Base):
    __tablename__ = 'user'

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


engine = create_engine(
    "mysql+pymysql://root:111@127.0.0.1:3306/ai?charset=utf8",
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


