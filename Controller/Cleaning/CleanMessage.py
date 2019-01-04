#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2018-12-01


import re

from Utils.Configuration import Configuration
from Model.MessageModel import MessageModel

class CleanMessage(object):
    """获取每条聊天记录的中的内容并将其分类"""
    def __init__(self, origTexts:str, formatedDatas:list, ignoredTexts:dict):
        self.origTexts = origTexts # 聊天记录字符串
        self.formatedDatas = formatedDatas # 存储清洗后内容的列表
        self.ignoredTexts = ignoredTexts # 存储清洗中要去掉的内容的字典
        # self.nameIDDct = {} # 存储ID、用户名的字典，用于ID去重或用户名去重


    def cleaning(self):
        """清洗聊天记录"""
        inTable = "\xa0\t" # 
        outTable = "  "
        transTable = str.maketrans(inTable, outTable)
        # self.origTexts = self.origTexts.translate(transTable) # 去掉不间断空白符等符号
        # 以日期、时间、昵称、QQ作为分割符(保留分隔符)拆分聊天记录
        textLst = re.split('(20\d{2}-\d{2}-\d{2} \d{1,2}:\d{2}:\d{2}\s+[^\n]*)', self.origTexts)[1:]
        i = 0
        while(i < len(textLst)):
            authorText = textLst[i].strip() # 答题时间
            contentText = textLst[i+1].strip()  # 发言信息
            msg = MessageModel('0', '0000-00-00', '00:00:00', '0', '')
            if re.match(Configuration.themeInfo['tag'] + Configuration.themeInfo['term'], contentText):
                if(self.cleaning_contentText(authorText, contentText, msg)==1 and 
                    len(msg.content)>Configuration.themeInfo['wordsNumRequired']): # 清洗答题信息
                    self.formatedDatas.append(msg)
                    # print(msg)
            i += 2
        #--END while
        return 1


    def cleaning_contentText(self, authorText:str, contentText:str, msg):
        """清洗信息"""
        #-- 从答题人信息中获取日期、时间、QQ
        tempLst = re.split('(20\d{2}-\d{2}-\d{2} \d{1,2}:\d{2}:\d{2})', authorText)
        [msg.msgdate, msg.msgtime] = tempLst[-2].split(" ")
        #-- 从答题人信息中获取昵称和ID
        try: # ID是QQ号
            tempLst = re.split('(\(\d{6,13}\))', tempLst[-1])
            msg.qqID = tempLst[1][1:-1]
            # msg.authorname = tempLst[0].strip()
        except Exception as e:
            try: # ID是邮箱
                tempLst = re.split("(<[\w\.-]{3,20}@[\w\.-]{2,20}\.\w{2,4}>)", tempLst[-1])
                msg.qqID = tempLst[1][1:-1]
                # msg.authorname = tempLst[0].strip()
            except Exception as e:
                try: # ID类似<13420967400>
                    tempLst = re.split('(<\d{6,13}\>)', tempLst[-1])
                    msg.qqID = tempLst[1][1:-1]
                    # msg.authorname = tempLst[0].strip()
                except Exception as e: # 未识别的ID
                    # print('未识别的ID：', authorText)
                    pass
        if (msg.qqID == '2109723514'):
            return 0
        if (msg.qqID == 'scalerstalk@gmail.com'):
            return 0

        #-- 清洗发言信息中的答题信息
        try:
            # contentText = re.sub('\s', " ", contentText) # 去除不同编码的空格的影响????????
            dayFlag = re.search('(Day [0-9]{1,3} [0-9]{1,2}\.[0-9]{1,2})', contentText).group()
            msg.dayFlag = dayFlag
            # print(dayFlag, self.ignoredTexts[dayFlag])
            try:
                for item in self.ignoredTexts[dayFlag]:
                    contentText =  contentText.replace(item, '$$$')
                contentText = contentText.replace('@全体成员', '$$$')
                contentText = re.split('\$\$\$', contentText)
                # contentText = list(set(contentText).difference(self.ignoredTexts[dayFlag])) # ???
                msg.dayFlag = dayFlag
                contentText = list(map(lambda x: x.strip(), contentText))
                msg.content = "".join(list(filter(lambda x: len(x)>1, contentText)))
            except Exception as e: # dayFlag 异常
                try:
                    if(dayFlag=='Day 1 9.4'):
                        ontentText = contentText.replace(dayFlag, '$$$')
                        dayFlag = 'Day 2 9.4'
                    elif(dayFlag=='Day 29 10.01'):
                        contentText = contentText.replace(dayFlag, '$$$')
                        dayFlag = 'Day 29 10.1'
                    for item in self.ignoredTexts[dayFlag]:
                        contentText =  contentText.replace(item, '$$$')
                    contentText = contentText.replace('@全体成员', '$$$')
                    contentText = re.split('\$\$\$', contentText)
                    # contentText = list(set(contentText).difference(self.ignoredTexts[dayFlag])) # ???
                    msg.dayFlag = dayFlag
                    contentText = list(map(lambda x: x.strip(), contentText))
                    contentText = "".join(list(filter(lambda x: len(x)>1, contentText)))
                    msg.content = contentText
                except Exception as e:
                    # print('任务中没有包含的dayFlag：', dayFlag)
                    return 0
                    pass
                pass
            # print(dayFlag, msg.content)
        except Exception as e:
            # print('未识别的信息')
            pass
        return 1



class CleanMessageProcess(object):
    """多进程清洗数据"""
    def __init__(self, msgLst:list, taskDct:dict):
        # self.origDatas = origDatas
        self.msgLst = msgLst
        self.taskDct = taskDct


    def cleaning_processPool(self):
        """数据清洗多进程控制"""
        inputsLst = GetInputs().get_inputs("inputs\\tasks\\")
        cleanTsk = CleanTask(''.join(inputsLst), self.taskDct)
        cleanTsk.cleaning_taskText()
        print('任务数量：', len(self.taskDct))

        origDatas = GetInputs().get_inputs("samples0\\records\\")

        # 定义线程池并创建线程对象
        myPool = multiprocessing.Pool()
        for origData in origDatas:
            myPool.apply_async(CleanMessage(origData, msgLst, taskDct).cleaning(), (origData,))  #增加新的进程
        myPool.close() # 禁止再增加新的进程
        myPool.join()
        print('清洗后的数据条数：', len(msgLst))
        return 1




class CleanMessageThread(object):
    """多线程清洗数据"""
    def __init__(self, msgLst:list, taskDct:dict):
        # self.origDatas = origDatas
        self.msgLst = msgLst
        self.taskDct = taskDct


    def cleaning_threadPool(self):
        """数据清洗多线程控制"""
        inputsLst = GetInputs().get_inputs("inputs\\tasks\\")
        cleanTsk = CleanTask(''.join(inputsLst), self.taskDct)
        cleanTsk.cleaning_taskText()
        print('任务数量：', len(self.taskDct))

        origDatas = GetInputs().get_inputs("inputs\\records\\")

        # 定义线程池并创建线程对象
        threads = []
        for origData in origDatas:
            cleanMsg = CleanMessage(origData, msgLst, taskDct)
            threads.append(threading.Thread(target=cleanMsg.cleaning(), args=(origData,)))  # 创建线程
        for thrd in threads: # 启动所有线程
            thrd.start()
        for thrd in threads: # 等待线程运行完毕
            thrd.join()
        print('清洗后的数据条数：', len(msgLst))
        return 1    
        

