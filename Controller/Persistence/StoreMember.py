#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2018-12-22

from Controller.DBController import DBInit
from Model.MemberModel import MemberModel


class StoreMember(object):
    """ 将消息保存在数据"""
    def __init__(self, dbCtrl):
        self.dbCtrl = dbCtrl

    def store_member(self, dataLst):
        try:
            # self.dbCtrl.dbSession.add_all(dataLst) # 要求列表元素为类
            dataDicLst = [item.__dict__ for item in dataLst] # 将类转化为字典
            # self.dbCtrl.dbSession.bulk_insert_mappings(MemberModel, dataDicLst)  # 要求列表元素为字典
            self.dbCtrl.dbSession.execute(MemberModel.__table__.insert().prefix_with('IGNORE'), dataDicLst)   # 要求列表元素为字典
            self.dbCtrl.dbSession.commit()
        except Exception as e:
            self.dbCtrl.dbSession.rollback()
            raise
        else:
            # print('插入' + str(len(dataLst)) + '个数据')
            pass
        finally:
            self.dbCtrl.dbSession.close()
