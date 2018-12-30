#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2018-12-01

import os
import re
# import threading
# import datetime


class Configuration(object):
    """docstring for Configuration"""
    themeInfo = {
        'tag': '#早起读书现学现卖#',
        'term': '第6期“财报与财富”专题',
        'day': 'Day',
        'books': ['用生活常识读懂财务报表', '轻松读懂财报', '五大关键数字力', '穿透财报', 
                '证券分析'],
        'tip': '（答题时，作业头不要修改，问题不要删除，统计时我们会核减作业字数）',
        'wordLen': 200
    }
    # ThreadInfo = {
    #     'mutex': threading.Lock(), # 创建线程锁
    #     'threadMaxnum': threading.Semaphore(4)  # 限制线程的最大数量
    # }



class GetInputs(object):
    """获取inputs的文件内容存储在列表中，每个文件的内容为列表的一个元素"""
    @staticmethod
    def get_inputs(filesDir:str) -> 'list of str':
        """获取文件夹中文件的文件内容，每个文件内容以str存入List，返回List"""
        inputsLst = []
        for dirpath, dirnames, filenames in os.walk(filesDir):
            for filename in filenames:
                # print(os.path.join(filesDir,filename))
                with open(os.path.join(filesDir,filename), encoding="UTF-8") as fhand:
                    inputsLst.append(fhand.read())
        return inputsLst



class CleanMessage(object):
    """获取每条聊天记录的中的内容并将其分类"""
    def __init__(self):
        # 以日期时间、昵称、QQ作为分割符(保留分隔符)得到聊天记录的列表
        self.userRegex = '(20\d{2}-\d{2}-\d{2}\s+\d{1,2}:\d{2}:\d{2}\s+[^\n]*)'
        self.titleRegex = '(P\d{1,3}-\d{1,3})'
        self.verifyRegex = Configuration.themeInfo['tag'] + Configuration.themeInfo['term'] + \
            Configuration.themeInfo['day'] + ' ' + '\d{1,3}'
        self.MsgLst = []
        self.QuestLst = [[], [], []]


    def clean_messages(self, recordsLst: 'list of str'):
        """清洗聊天记录"""
        # 定义线程池并创建线程对象
        # threads = [threading.Thread(target=self.clean_message, args=(recordsStr,)) 
        #     for recordsStr in recordsLst] # 创建线程
        # for thrd in threads: # 启动所有线程
        #     thrd.start()
        # for thrd in threads: # 等待线程运行完毕
        #     thrd.join()

        for recordsStr in recordsLst:
            self.clean_message(recordsStr)
        print("完成任务次数：%d；任务数量：%d" % (len(self.MsgLst), len(self.QuestLst[0])))
        print(self.QuestLst)
        # print(self.MsgLst[0:5])


    def clean_message(self, recordsStr:str):
        """检查聊天记录是否符合要求，并获取合格的聊天记录的详细信息"""
        recordLst = re.split(self.userRegex, recordsStr)[1:]
        # print(recordLst)
        i = 0
        while(i < len(recordLst)):
            user = recordLst[i] # 答题人信息
            assignment = recordLst[i+1] # 任务
            Msg = {
                'userid': '0000',
                'username': '----',
                'msgdate': '0000-00-00',
                'msgtime': '00:00:00'
            }
            #-- 保留正常的聊天数据。异常聊天记录将被剔除，例如没有发言时间、QQ、昵称，内容不合格等
            try: 
                #-- 从答题人信息中获取详细信息
                tempLst = re.split('(20\d{2}-\d{2}-\d{2} \d{1,2}:\d{2}:\d{2})', user)
                # print(tempLst)
                Msg['msgdate'] = tempLst[-2].split(" ")[0]
                Msg['msgtime'] = tempLst[-2].split(" ")[1]
                # print(re.findall('\d{5,12}', tempLst[-1])[0])
                Msg['userid'] = re.findall('\d{5,12}', tempLst[-1])[0]
                tempLst = re.split('\(\d{5,12}\)', tempLst[-1])
                Msg['username'] = tempLst[-2].strip()
                #-- 从任务中获取详细信息
                tempLst = re.split(self.titleRegex, assignment)
                # print(tempLst)
                title = (tempLst[0]+tempLst[1]).strip() # 标题信息
                content = tempLst[-1] # 任务内容
                if self.verify_assignment(title, content) == 1:
                    tempLst = re.split('\s', title)
                    Msg['dayNo'] = tempLst[1]
                    Msg['assigndate'] = re.search('\d{1,2}.\d{1,2}', tempLst[2]).group()
                    tempLst = re.split('\n(\d).', content)[1:]
                    question, answer = dict(), dict()
                    j = 0
                    while(j < len(tempLst)):
                        temp = re.split('\n', tempLst[j+1])
                        question['title'] = title
                        question[tempLst[j]] = temp[0]
                        answer[tempLst[j]] = "".join(temp[1:])
                        j += 2
                    # Configuration.ThreadInfo['mutex'].acquire() # 取得锁
                    if Msg['dayNo'] not in self.QuestLst[0]:
                        self.QuestLst[0].append(Msg['dayNo'])
                        self.QuestLst[1].append(Msg['assigndate'])
                        self.QuestLst[2].append(question)
                    # Configuration.ThreadInfo['mutex'].release() # 释放锁
                    Msg['answer'] = answer
                    if (Msg['userid'] != '2109723514') and (Msg['userid'] != '1099050085'): # 发布任务的消息不作分析
                        self.MsgLst.append(Msg)
            except:
                # print('Error: ' + user + assignment)
                pass
            finally:
                i += 2
        #-- End While
        # print("thread-%s ended %s" % (threading.current_thread().name, datetime.datetime.now()))


    def verify_assignment(self, title:str, content:str) -> int:
        """检查任务内容是否符合要求。
           return: 1-合格，0-不合格""" 
        if not re.match(self.verifyRegex, title):
            return 0
        findBookFlag = 0 # 书有多本，使用特定的标志位帮助检查书名：1-找到书名，0-未找到书名
        for book in Configuration.themeInfo['books']:
            if re.search(book, title):
                findBookFlag = 1
        if findBookFlag == 0:
            return 0
        return 1
        



if __name__ == '__main__':
    # print("begin %s" % (datetime.datetime.now()))
    # inputsLst = GetInputs().get_inputs("samples\\")
    inputsLst = GetInputs().get_inputs("inputs\\")
    msgLst = CleanMessage().clean_messages(inputsLst)
    

