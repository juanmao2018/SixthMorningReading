#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2018-1226

from sqlalchemy.orm import aliased
from sqlalchemy import text, case, outerjoin, func
import pandas as pd
import numpy as np
import datetime, threading
from decimal import *

from Utils.Configuration import Configuration
from Model.MessageModel import MessageModel
from Model.MemberModel import MemberModel

Message = aliased(MessageModel, name='Message')
Member = aliased(MemberModel, name='Member')


class AnalyseMember(object):
    """打卡成员分析"""
    def __init__(self, DBCtrl):
        self.DBCtrl = DBCtrl
        self.memberLst = None # 成员列表
        self.peopleNum_wordNum_everyday = None # 每天的打卡人数和字数（一个人一天多次打卡仅统计一次）
        self.dayNum_wordNum_rank = None # 每个用户的打卡天数、字数，并排名（按照天数、字数降序排列，一天多次打卡算一次）
        self.description = ''
        self.individualResults = None # 个人分析的结果列表


    def get_memberLst(self):
        """查询成员列表"""
        rows = None
        try:
            rows = self.DBCtrl.dbSession.query(Message.qqID.distinct(), Member.qqName, 
                Member.nickname, Member.email, Member.label, Member.city, Member.job)\
                .outerjoin(Member, Message.qqID == Member.qqID).all()
            rows = pd.DataFrame(rows, index=range(1,len(rows)+1), 
                columns=['qqID', 'qqName', 'nickname', 'email', 'label', 'city', 'job'])
            self.memberLst = rows
        except Exception as e:                
            print('!Error: 没有查询到信息')
            raise e
        # print(rows)
        return rows


    def get_peopleNum_wordNum_everyday(self):
        """查询每天的打卡人数和字数（一个人一天多次打卡仅统计一次）"""
        rows = None
        try:
            rows = self.DBCtrl.dbSession.query(Message.msgdate, 
                func.count(Message.qqID.distinct()).label('peopleNum'), 
                func.sum(func.length(Message.content)).label('wordNum')).group_by(Message.msgdate).all()
            rows = pd.DataFrame(rows, index=range(1,len(rows)+1), 
                columns=['date', 'peopleNum', 'wordNum'])
            rows.set_index(["date"], inplace=True) # 指定某一列的值作为索引
            self.peopleNum_wordNum_everyday = rows
        except Exception as e:
            print('没有查询到每天的打卡人数和字数信息')
            raise e
        # print(rows)
        return rows


    def get_dayNum_wordNum_rank(self):
        """查询每个用户的打卡天数、字数，并排名（按照天数、字数降序排列，一天多次打卡算一次）"""
        rows = None
        # try: # 用SQL的order by语句排名
        #     stmt = self.DBCtrl.dbSession.query(Message.qqID, func.count(Message.msgdate.\
        #         distinct()).label('dayNum')).group_by(Message.qqID).subquery()
        #     stmt2 = self.DBCtrl.dbSession.query(Message.qqID, func.sum(func.length(Message.content)).\
        #         label('wordNum')).group_by(Message.qqID).subquery()
        #     rows = self.DBCtrl.dbSession.query(stmt.c.qqID, stmt.c.dayNum, 
        #         stmt2.c.wordNum).filter(stmt.c.qqID==stmt2.c.qqID).\
        #         order_by(stmt.c.dayNum.desc(), stmt2.c.wordNum.desc()).all()
        #     rows = pd.DataFrame(rows, index=range(1,len(rows)+1), 
        #         columns=['qqID', 'dayNum', 'wordNum'])
        #     rows.index.names = ['rank']
        #     self.dayNum_wordNum_rank = rows
        # except Exception as e:
        #     print('!Error: 没有查询到信息')
        #     raise e
        # print(rows)
        try: # 用DataFrame的sort_values()排名
            stmt = self.DBCtrl.dbSession.query(Message.qqID, func.count(Message.msgdate.\
                distinct()).label('dayNum')).group_by(Message.qqID).subquery()
            stmt2 = self.DBCtrl.dbSession.query(Message.qqID, func.sum(func.length(Message.content)).\
                label('wordNum')).group_by(Message.qqID).subquery()
            rows = self.DBCtrl.dbSession.query(stmt.c.qqID, stmt.c.dayNum, 
                stmt2.c.wordNum).filter(stmt.c.qqID==stmt2.c.qqID).all()
            rows = pd.DataFrame(rows, columns=['qqID', 'dayNum', 'wordNum'])
            rows = rows.sort_values(by=['dayNum','wordNum'], ascending=[False, False])
            rows['rank'] = range(1,len(rows)+1)
            self.dayNum_wordNum_rank = rows
        except Exception as e:
            print('!Error: 没有查询到信息')
            raise e
        # print(rows)
        return rows


    def get_rank_by_qqID(self, qqID):
        """通过用户号获取打卡排名、超越的百分比"""
        rank = (0, 0)
        try:
            rankNum = self.dayNum_wordNum_rank[self.dayNum_wordNum_rank['qqID']==qqID].\
                index.tolist()[0]
            rank = (rankNum, 1 - rankNum/len(self.dayNum_wordNum_rank))
        except Exception as e:
            print('没有该用户的排名信息', qqID, rank)
        # print(rank)
        return rank


    def get_name_by_qqID(self, qqID):
        """通过用户号获取用户名"""
        name = ''
        try:
            if '@' in qqID:
                name = qqID.split('@')[0]
            else:
                name = list(self.memberLst[self.memberLst['qqID']==qqID]['nickname'])[0]
                if name is None:
                    name = list(self.memberLst[self.memberLst['qqID']==qqID]['qqName'])[0]
                    if name is None:
                        name = ''
        except Exception as e:
            print('没有该用户的用户名', qqID)
            raise e
        # print(name)
        return name


    def get_description(self):
        """描述分析结果"""
        description = ''
        description += '    %s%s活动自%s开始，\n阅读了书籍：' % (Configuration.themeInfo['tag'], 
            Configuration.themeInfo['term'], min(self.peopleNum_wordNum_everyday.index))
        description += ''.join(Configuration.themeInfo['books'])
        description += '。\n在这%s天中，共有%s人参与打卡。' % (len(self.peopleNum_wordNum_everyday), 
            len(self.dayNum_wordNum_rank))
        description += '\n每天打卡的人数及输出的文字数量如下图：'
        self.description = description
        # print(description)
        return description


    def get_analyse_individual_result(self, targetMembers=[]):
        """查询目标列表中的个体分析结果"""
        resultLst = []
        if len(targetMembers) == 0:
            targetMembers = self.memberLst['qqID']
        # print(targetMembers)
        for item in targetMembers:
            self.get_analyse_individual(item, resultLst)
        self.individualResults = resultLst
        return resultLst


    def get_analyse_individual(self, targetQQID, resultLst):
        """查询个体分析结果"""
        name = self.get_name_by_qqID(targetQQID)
        rank = self.get_rank_by_qqID(targetQQID)
        anlsIndvMember = AnalyseIndividualMember(self.DBCtrl, targetQQID, name, rank)
        rows = anlsIndvMember.get_wordNum_everyday()
        anlsIndvMember.get_description()
        resultLst.append(anlsIndvMember) 
        return 1


    def get_analyse_individual_result_multiThread(self, targetMembers=[]):
        """多线程实现查询目标列表中的个体分析结果"""
        resultLst = []
        if len(targetMembers) == 0:
            targetMembers = self.memberLst['qqID']
        # 定义线程池并创建线程对象
        threads = [threading.Thread(target=self.get_analyse_individual_thread, 
            args=(item, resultLst)) for item in targetMembers] # 创建线程
        for thrd in threads: # 启动所有线程
            thrd.start()
        for thrd in threads: # 等待线程运行完毕
            thrd.join() 
        self.individualResults = resultLst
        return resultLst


    def get_analyse_individual_thread(self, targetQQID, resultLst):
        """查询个体分析结果"""
        with Configuration.ThreadInfo['threadMaxnum']:
            name = self.get_name_by_qqID(targetQQID)
            rank = self.get_rank_by_qqID(targetQQID)
            # print("thread-%s is running %s" % (threading.current_thread().name, datetime.datetime.now()))
            anlsIndvMember = AnalyseIndividualMember(self.DBCtrl, targetQQID, name, rank)
            anlsIndvMember.get_wordNum_everyday()
            anlsIndvMember.get_description()
            Configuration.ThreadInfo['mutex'].acquire() # 取得锁
            resultLst.append(anlsIndvMember) 
            Configuration.ThreadInfo['mutex'].release() # 释放锁
            # print("thread-%s ended %s" % (threading.current_thread().name, datetime.datetime.now()))
            return 1
        

    def __repr__(self):
        return "<%s(descrip=%s)>" % (self.__class__.__name__, self.descrip)
        
        

class AnalyseIndividualMember(object):
    """个人分析"""
    def __init__(self, DBCtrl, qqID, qqName, rank):
      self.DBCtrl = DBCtrl
      self.qqID = qqID
      self.rank = rank
      self.qqName = qqName
      self.wordNum_everyday = None
      self.description = ''


    def get_wordNum_everyday(self):
        """查询指定用户号的每天的打卡字数"""
        rows = None
        try:
            stmt = self.DBCtrl.dbSession.query(Message.msgdate.distinct().label('msgdate')).order_by(Message.msgdate).subquery()
            stmt2 = self.DBCtrl.dbSession.query(Message.msgdate.distinct().label('msgdate'), func.sum(func.length(Message.content)).label('wordNum')).\
                filter(Message.qqID==self.qqID).group_by(Message.msgdate).subquery()
            rows = self.DBCtrl.dbSession.query(stmt.c.msgdate, stmt2.c.wordNum).outerjoin(stmt2, stmt.c.msgdate == stmt2.c.msgdate).all()
            rows = pd.DataFrame(rows, columns=['date', 'wordNum'])
            rows.index = rows['date'].tolist()
            rows.set_index(["date"], inplace=True) # 指定某一列的值作为索引
            rows['wordNum'] = rows['wordNum'].map(lambda x: 0 if x is None else x)
            self.wordNum_everyday = rows
            # print(rows)
        except Exception as e:
            print('没有该用户的打卡信息', self.qqID)
            self.DBCtrl.dbSession.rollback()
            raise e
        return rows


    def get_description(self):
        """描述分析结果"""
        description = '亲爱的%s(%s)：' % (self.qqName, self.qqID[0:2]+'*'*4+self.qqID[-3:])
        description += '\n    你好!\n    %s%s自%s开始，' % (
            Configuration.themeInfo['tag'], Configuration.themeInfo['term'], 
            min(self.wordNum_everyday.index))
        description += '\n在这%s天中，你参与打卡%s天, 共输出%s字。' % (len(self.wordNum_everyday), 
            len(self.wordNum_everyday[self.wordNum_everyday['wordNum'] > 0]),
            np.sum(self.wordNum_everyday['wordNum']))
        description += '\n在打卡排名中位列%s，超过了%.2f%%的小伙伴\\(^o^)/~' % (self.rank[0], self.rank[1]*100)
        description += '\n每天输出的文字数量如下图：'
        self.description = description
        # print(description)
        return description