#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2018-12-22


import re

# from Utils.Configuration import Configuration
from Model.MemberModel import MemberModel


class CleanMember(object):
    """清洗成员信息"""
    def __init__(self, origTexts:str, formatedDatas:list):
        self.origTexts = origTexts
        self.formatedDatas = formatedDatas


    def cleaning(self):
        """清洗记录"""
        inTable = "\xa0\t" # 
        outTable = "  "
        transTable = str.maketrans(inTable, outTable)
        # 以日期、时间、昵称、QQ作为分割符(保留分隔符)拆分聊天记录
        textLst = re.findall('20\d{2}-\d{2}-\d{2} \d{1,2}:\d{2}:\d{2}\s+(.*)\n', self.origTexts)[1:]
        textLst = list(set(textLst))
        # print(textLst)
        tempLst = ['', '']
        for item in textLst:
            memb = MemberModel('', '', '', '', '', '', '')
            try: # ID是QQ号
                tempLst = re.split('(\(\d{6,13}\))', item)
                memb.qqID = tempLst[1][1:-1].strip()
                memb.qqName = authorname = tempLst[0].strip()
            except Exception as e:
                try: # ID是邮箱
                    tempLst = re.split("(<[\w\.-]{3,20}@[\w\.-]{2,20}\.\w{2,4}>)", item)
                    memb.qqID = memb.email = tempLst[1][1:-1].strip()
                    memb.qqName = authorname = tempLst[0].strip()
                except Exception as e:
                    try: # ID类似<13420967400>
                        tempLst = re.split('(<\d{6,13}\>)', item)
                        memb.qqID = tempLst[1][1:-1].strip()
                        memb.qqName = authorname = tempLst[0].strip()
                    except Exception as e: # 未识别的ID
                        # print('未识别的ID：', authorText)
                        pass    
            

            tempLst = re.split('[-~_\+]+', authorname)
            if re.search('[\[【]?[Ss]\d{1,4}', authorname): # S会员
                memb.label = 'S' # S
                temp = re.split('[\[【]?([Ss]?\d{1,4})[\]】]?', tempLst[0])
                memb.nickname = temp[-1].strip()
                if(len(tempLst)==3):
                    memb.city = tempLst[-1]
                    memb.job = tempLst[-2]
            elif '游学' in authorname:  # 游学
                memb.label = 'Y'
                if(len(tempLst)==3):
                    memb.nickname = tempLst[1]
                    memb.city = tempLst[-1]
            else:  # unknown
                memb.label = 'U'
            # print(memb)
            if (memb.qqID != '2109723514') and (memb.qqID != 'scalerstalk@gmail.com') \
                and(memb.qqID != '1000000'):
                self.formatedDatas.append(memb)
        #-- END for
        return 1
        