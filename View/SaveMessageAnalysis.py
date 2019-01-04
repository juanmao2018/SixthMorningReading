#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2018-12-28

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
plt.switch_backend('agg') 
# myfont = matplotlib.font_manager.FontProperties(fname=r'C:/Windows/Fonts/SimHei.ttf') 
plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
import time, multiprocessing

from Controller.Analysis.AnalyseMember import AnalyseMember
from Controller.Analysis.AnalyseMember import AnalyseIndividualMember
from Utils.Configuration import Configuration


class SaveMessageAnalysis(object):
    """保存MessageAnalysis类的分析结果到文件"""
    def __init__(self, outpath='outputs\\'):
        self.outpath = outpath


    def save_member_analysis(self, analMember, filename='分析结果'):
        """将分析结果保存到文件"""
        self.save_member_analysis_whole(analMember, '成员整体分析结果')
        self.save_member_analysis_individual(analMember.individualResults, '成员个体分析结果集')
        
        # individualResult = analMember.individualResults
        # print(len(individualResult))

        # for oneMember in analMember.individualResult:
        #     dataLst.append(oneMember.wordNum_everyday)
        #     sheetnams.append(oneMember.qqID + '每日打卡情况')
        #     memberNames.append(self.outpath + filename + oneMember.qqID \
        #         + Configuration.imgInfo['filetype'])
        # temp = zip(individualResult, memberNames)

        # list(procsPool.map(self.draw_members_analysis_individual, temp))
        # procsPool.close() 
        # procsPool.join() 
        return 1


    def save_member_analysis_whole(self, analMember, filename='成员整体分析结果'):
        """将整体的分析结果保存到文件"""
        dataLst, sheetnams = list(), list()
        if isinstance(analMember, AnalyseMember):
            #-- 组装EXCEL文件的内容
            dataLst = [
                analMember.memberLst, analMember.peopleNum_wordNum_everyday, 
                analMember.dayNum_wordNum_rank
            ]
            sheetnams = [
                '成员列表', '每日打卡用户数量和字数',
                '用户打卡天数和字数排名'
            ]
            SaveMessageAnalysis.save_to_excel(self.outpath+filename+'.xlsx', dataLst, sheetnams) # 存入EXCEL文件
            #-- 绘图
            self.draw_member_analysis_whole(analMember, self.outpath + filename) # 总体分析绘图
            return 1
        else:
            print("不是总体分析结果！")
            return 0


    def save_member_analysis_individual(self, results, filename='成员个体分析结果集'):
        """将成员个体分析结果集保存到文件"""
        dataLst, sheetnams, individualFilenames = list(), list(), list()
        for oneMember in results:
            dataLst.append(oneMember.wordNum_everyday)
            sheetnams.append(oneMember.qqID + '分析')
            # individualFilenames.append(self.outpath + filename + oneMember.qqID)
            # temp = zip(oneMember, self.outpath+filename+oneMember.qqID)
            if '@' in oneMember.qqID:
                tempname = oneMember.qqName[:4]
            else:
                tempname = oneMember.qqID
            self.draw_members_analysis_individual(oneMember, self.outpath+tempname)
        SaveMessageAnalysis.save_to_excel(self.outpath+filename+'.xlsx', dataLst, sheetnams) # 存入EXCEL文件
        return 0
        

    def draw_member_analysis_whole(self, analMember, filename='统计结果'):
        """将总体分析的结果绘图"""
        fig, axes = plt.subplots(2,1)
        ax1, ax2 = axes[0], axes[1]

        data = analMember.peopleNum_wordNum_everyday
        data['peopleNum'] = pd.to_numeric(data['peopleNum'])
        data['wordNum'] = pd.to_numeric(data['wordNum'])

        # -- 绘图：分析结果
        ax1.text(0.0, 0.5, analMember.description)
        ax1.axis('off')

        # -- 绘图：每日打卡用户数、打卡字数绘制在一张图中
        # -- 绘图：按照日期统计的打卡用户数
        lns1 =data['peopleNum'].plot(kind='line', ax=ax2, rot=90, 
            xticks=pd.date_range(start=min(data.index), end=max(data.index), freq='2D'),
            ylim=[0, max(data['peopleNum'])])
        # -- 绘图：按照日期统计的打卡字数
        ax2_twins = ax2.twinx()  # 双y轴绘制
        lns2 = data['wordNum'].plot(kind='line', ax=ax2_twins, rot=90, color='r',
            xticks=pd.date_range(start=min(data.index), end=max(data.index), freq='2D'),
            ylim=[0, max(data['wordNum'])])
        fig.legend(loc=1, bbox_to_anchor=(1,1), bbox_transform=ax2.transAxes) # 合并图例
        date_format = mpl.dates.DateFormatter("%m/%d")
        ax2.xaxis.set_major_formatter(date_format)
        # plt.show()
        plt.savefig(filename, bbox_inches='tight')
        plt.close()
        return 1


    def draw_members_analysis_individual(self, oneMember, filename):
        """将个人分析的结果绘图"""
        # print("Starting draw_individual_members_analysis() " + oneMember.qqID + " " + time.ctime())
        fig, axes = plt.subplots(2,1)
        ax1, ax2 = axes[0], axes[1]
        data = oneMember.wordNum_everyday
        data.wordNum = pd.to_numeric(data.wordNum)

        #-- 绘图：分析结果
        ax1.text(0.0, 0.5, oneMember.description)
        ax1.axis('off')

        #-- 绘图：按照日期统计的打卡字数
        data['wordNum'].plot(kind='line', ax=ax2, rot=90, 
            xticks=pd.date_range(start=min(data.index), end=max(data.index), freq='2D'),
            ylim=[0, max(data['wordNum'])])
        date_format = mpl.dates.DateFormatter("%m/%d")
        ax2.xaxis.set_major_formatter(date_format)
        fig.legend(loc=1, bbox_to_anchor=(1,1), bbox_transform=ax2.transAxes)
        # plt.show()
        plt.savefig(filename, bbox_inches='tight')
        plt.close()
        return 1


    @staticmethod
    def save_to_excel(filename='result.xlsx', dataLst=[], sheetnams=[]):
        """数据保存在指定的EXCEL文件中，每个sheet按照要求命名"""
        if len(dataLst) != len(sheetnams):
            print('存入EXCEL的列表长度不一致，无法写入EXCEL文件')
            return 0
        fwriter = pd.ExcelWriter(filename)
        for i in range(len(sheetnams)):
            dataLst[i].to_excel(fwriter, sheetnams[i])
        fwriter.save()
        fwriter.close()
        return 1



