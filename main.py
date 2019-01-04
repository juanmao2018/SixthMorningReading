#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2018-12-13

from Controller.DBController import DBInit
from Controller.Cleaning.GetInputTexts import GetInputs
from Controller.Cleaning.CleanTask import CleanTask
from Controller.Cleaning.CleanMessage import CleanMessage
from Controller.Cleaning.CleanMember import CleanMember
from Controller.Persistence.StoreMessage import StoreMessage
from Controller.Persistence.StoreMember import StoreMember
from Controller.Analysis.AnalyseMember import AnalyseMember, AnalyseIndividualMember

from Model.MemberModel import MemberModel
from Model.MessageModel import MessageModel

from View.SaveMessageAnalysis import SaveMessageAnalysis

from Utils.Configuration import Configuration


def main():

    DBCtrl = DBInit()
    # DBCtrl.init_db() # -- 建表模型
    # DBCtrl.drop_db()

    # -- 清洗数据
    taskDct, membLst, msgLst= {}, [], []

    # inputsLst = GetInputs().get_inputs("inputs\\records\\")
    # cleanMemb = CleanMember(''.join(inputsLst), membLst)
    # cleanMemb.cleaning()
    # print('清洗后的成员数据条数：', len(membLst))
    # StoreMember(DBCtrl).store_member(membLst) # 数据入库
    # del membLst

    # inputsLst = GetInputs().get_inputs("inputs\\tasks\\")
    # cleanTsk = CleanTask(''.join(inputsLst), taskDct)
    # cleanTsk.cleaning_taskText()
    # print('任务数量：', len(taskDct))

    # inputsLst = GetInputs().get_inputs("inputs\\records\\")
    # cleanMsg = CleanMessage(''.join(inputsLst), msgLst, taskDct)
    # cleanMsg.cleaning()
    # print('清洗后的数据条数：', len(msgLst))
    # StoreMessage(DBCtrl).store_message(msgLst) # 数据入库
    # del msgLst

    #-- 成员总体分析
    analMember = AnalyseMember(DBCtrl)
    analMember.get_memberLst()
    analMember.get_peopleNum_wordNum_everyday()
    analMember.get_dayNum_wordNum_rank()
    analMember.get_description()
    result = analMember.get_analyse_individual_result([]) # 列表为空，所有的个体分析
    print(len(result))
    # a = analMember.get_rank_by_qqID('123456@qq.com')
    # analMember.get_name_by_qqID('123456@qq.com')

    #-- 成员个体分析
    # anlsIndvMember = AnalyseIndividualMember(DBCtrl, '123456@qq.com', 
    #     analMember.get_name_by_qqID('123456@qq.com'), analMember.get_rank_by_qqID('123456@qq.com'))
    # a = anlsIndvMember.get_wordNum_everyday()
    # # print(a)
    # anlsIndvMember.get_description()


    #-- 保存分析结果
    saveMemberAnal = SaveMessageAnalysis(Configuration.pathInfo['outputsPath'])
    saveMemberAnal.save_member_analysis(analMember)
    



if __name__ == '__main__':
    main()