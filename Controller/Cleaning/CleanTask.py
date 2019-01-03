#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2018-12-18

import re

from Utils.Configuration import Configuration


class CleanTask(object):
    """清洗任务信息"""
    def __init__(self, origTexts:str, taskDct:dict):
        self.origTexts = origTexts
        self.taskDct = taskDct


    def cleaning_taskText(self):
        """清洗任务文件中的任务信息"""
        textLst = re.split('('+ Configuration.themeInfo['tag'] + Configuration.themeInfo['term'] +')', self.origTexts)[1:]
        # print(textLst)
        i = 0
        while (i < len(textLst)):
            try: # 获取dayFlag，并将任务尽量拆成短句子
                contentLst = [Configuration.themeInfo['tag'], Configuration.themeInfo['term']]
                regexLst = [
                    # '(' + Configuration.themeInfo['tips'] + ')',
                    '(Day\s[0-9]{1,3}\s[0-9]{1,2}\.[0-9]{1,2})',
                    '(《\S+》)', # 书名
                    '(P\d{1,4}-\d{1,4})', # 页码
                    # '(\n\d[\., ]?)', # 题目的编号
                    '[\n,，,。,？,：]'] # 换行和标点
                dayFlag = re.search('Day\s[0-9]{1,3}\s[0-9]{1,2}\.[0-9]{1,2}', textLst[i+1]).group()
                tempLst = re.split('|'.join(regexLst), textLst[i+1])
                tempLst = list(map(lambda x: x.strip(' \n\t\r\f\v') if(isinstance(x,str)) else '', tempLst))
                tempLst = list(filter(lambda x: len(x)>0, tempLst))
                contentLst.extend(list(set(tempLst)))
                self.taskDct[dayFlag] = contentLst
                # print(dayFlag, contentLst)
            except Exception as e:
                # print('未识别的任务信息！')
                raise e
                pass
            i += 2
        self.taskDct['Day 1 9.3'].append('《用生活常识读懂财务报表》')
        self.taskDct['Day 2 9.4'].append('《用生活常识读懂财务报表》')
        self.taskDct['Day 3 9.5'].append('《用生活常识读懂财务报表》')
        self.taskDct['Day 4 9.6'].append('《用生活常识读懂财务报表》')
        self.taskDct['Day 5 9.7'].append('《用生活常识读懂财务报表》')
        #--END while
        return 1