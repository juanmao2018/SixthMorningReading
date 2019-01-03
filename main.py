#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2018-12-13

# from Controller.DBController import DBController
from Controller.DBController import DBInit
from Controller.Cleaning.GetInputTexts import GetInputs
from Controller.Cleaning.CleanTask import CleanTask
from Controller.Cleaning.CleanMessage import CleanMessage
from Controller.Cleaning.CleanMember import CleanMember
from Controller.Persistence.StoreMessage import StoreMessage
from Controller.Persistence.StoreMember import StoreMember
# from Controller.Analysis.AnalyseAuthor import AnalyseAuthor

from Model.MemberModel import MemberModel
from Model.MessageModel import MessageModel


def main():

    DBCtrl = DBInit()
    DBCtrl.init_db() # -- 建表模型
    # DBCtrl.drop_db()

    # -- 清洗数据
    taskDct, membLst, msgLst= {}, [], []

    # inputsLst = GetInputs().get_inputs("inputs\\tasks\\")
    # cleanTsk = CleanTask(''.join(inputsLst), taskDct)
    # cleanTsk.cleaning_taskText()
    # print('任务数量：', len(taskDct))

    # inputsLst = GetInputs().get_inputs("inputs\\records\\")
    # cleanMemb = CleanMember(''.join(inputsLst), membLst)
    # cleanMemb.cleaning()
    # print('清洗后的成员数据条数：', len(membLst))
    # StoreMember(DBCtrl).store_member(membLst) # 数据入库
    # del membLst

    # inputsLst = GetInputs().get_inputs("inputs\\records\\")
    # cleanMsg = CleanMessage(''.join(inputsLst), msgLst, taskDct)
    # cleanMsg.cleaning()
    # print('清洗后的数据条数：', len(msgLst))
    # StoreMessage(DBCtrl).store_message(msgLst) # 数据入库
    # del msgLst
    



if __name__ == '__main__':
    main()