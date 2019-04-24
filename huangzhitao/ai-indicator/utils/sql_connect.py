# -*- coding:utf-8 -*-
# @Time :2019/4/18 14:58
__author__ = "HuangZhiTao"


import pymysql
from settings import MYSQL_CONNECT


class SqlConnect:
    def __init__(self):
        self.conn = pymysql.connect(
            host=MYSQL_CONNECT["host"], user=MYSQL_CONNECT["user"], password=MYSQL_CONNECT["passwd"],
            database=MYSQL_CONNECT["database"], charset=MYSQL_CONNECT["charset"]
        )
        self.cur = self.conn.cursor()

    def __del__(self):
        self.cur.close()
        self.conn.close()


db = SqlConnect()

