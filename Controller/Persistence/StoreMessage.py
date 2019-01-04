#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2018-10-29

from Controller.DBController import DBInit
from Model.MessageModel import MessageModel

class StoreMessage(object):
    """ 将消息保存在数据"""
    def __init__(self, DBCtrl):
        self.DBCtrl = DBCtrl

    def store_message(self, msgLst):
        try:
            # self.DBCtrl.dbSession.add_all(msgLst) # 要求列表元素为类
            msgDctLst = [item.__dict__ for item in msgLst] # 将类转化为字典
            # self.DBCtrl.dbSession.bulk_insert_mappings(MessageModel, msgDctLst)  # 要求列表元素为字典
            self.DBCtrl.dbSession.execute(MessageModel.__table__.insert().prefix_with('IGNORE'), msgDctLst)   # 要求列表元素为字典
            self.DBCtrl.dbSession.commit()
        except Exception as e:
            self.DBCtrl.dbSession.rollback()
            raise
        else:
            # print('插入' + str(len(msgLst)) + '个数据')
            pass
        finally:
            self.dbCtrl.dbSession.close()
