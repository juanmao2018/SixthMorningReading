#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2018-10-29
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


from Model.MemberModel import MemberModel
from Model.MessageModel import MessageModel

Base = declarative_base()

class DBInit(object):
    """数据库配置信息、初始化类"""
    def __init__(self):
        DBInfo = {
            'HOSTNAME' : 'localhost',
            'PORT' : '3306',
            'DATABASE' : 'test',
            'USERNAME' : 'test',
            'PASSWORD' : '123456'
        }
        self.DB_URI = "mysql+pymysql://%(USERNAME)s:%(PASSWORD)s@%(HOSTNAME)s:%(PORT)s/%(DATABASE)s" % DBInfo
        self.engine = create_engine(self.DB_URI, max_overflow=5, echo=False) # Connecting
        self.Session = sessionmaker(bind=self.engine)
        self.dbSession = self.Session()


    def init_db(self):
        """定义初始化数据库函数"""
        Base.metadata.create_all(self.engine, tables=[MemberModel.__table__, MessageModel.__table__]) # Create a Schema


    def drop_db(self):
        """删除数据库函数"""
        Base.metadata.drop_all(self.engine, tables=[MemberModel.__table__, MessageModel.__table__])





# class DBController(DBInit):
#     """数据库控制类"""
#     def init_db(self):
#         """定义初始化数据库函数"""
#         Base.metadata.create_all(self.engine) # Create a Schema


#     def drop_db(self):
#         """删除数据库函数"""
#         Base.metadata.drop_all(self.engine)