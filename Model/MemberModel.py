#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2018-12-22

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, Time, Text, Integer, UniqueConstraint

Base = declarative_base()  # create the base class

class MemberModel(Base):
    """定义映射关系类MemberModel"""
    __tablename__ = 'six_member' # 表名
    # 字段
    memberid = Column(Integer, primary_key=True, autoincrement=True) # 用户的主键
    qqID = Column(String(64), nullable=False) # 用户编号
    qqName = Column(String(100)) # 用户名称
    nickname = Column(String(100)) # 用户昵称
    email = Column(String(64)) # 邮箱
    label = Column(String(1), comment="S-'S'；Y-'游学'；U-'未知'") # S-'S'；Y-'游学'；U-'未知'
    city = Column(String(64)) # 城市
    job = Column(String(64)) # 工作


    def __init__(self, qqID:str, qqName:str, nickname:str, email:str, label:str, city:str, job:str):
        self.qqID = qqID
        self.qqName = qqName
        self.nickname = nickname
        self.email = email
        self.label = label
        self.city = city
        self.job = job
        

    def __repr__(self):
        return "<%s(qqID='%s', qqName=%s, nickname=%s, email='%s', label='%s', city='%s',  job='%s')>" % (
            self.__class__.__name__, self.qqID, self.qqName, self.nickname, self.email, 
            self.label, self.city, self.job)
   



# class MessageModel(Base):
#     """定义映射关系类MessageModel"""
#     __tablename__ = 'six_message' # 表名
#     # 字段
#     msgid = Column(Integer, primary_key=True, autoincrement=True) # 消息的主键
#     qqID = Column(String(64), nullable=False) # 用户编号
#     msgdate = Column(Date) # 消息发送日期
#     msgtime = Column(Time) # 消息发送时间
#     dayFlag = Column(String(20)) # 任务对应的日期标志
#     content = Column(Text, nullable=False)
#     __table_args__ = (UniqueConstraint(msgdate, msgtime, name='msgUnique'), ) # 消息去重


#     def __init__(self, qqID:str, msgdate:str, msgtime:str, dayFlag:str, content=None):
#         self.qqID = qqID
#         self.msgdate = msgdate
#         self.msgtime = msgtime
#         self.dayFlag = dayFlag
#         self.content = content
        

#     def __repr__(self):
#         return "<%s(qqID='%s', msgdate=%s, msgtime='%s', contentLen='%s', dayFlag='%s')>" % (
#             self.__class__.__name__, self.qqID, self.msgdate, self.msgtime, 
#             len(self.content), self.dayFlag,)
   

   

   