#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2018-12-18

import threading

class Configuration(object):
    """程序的常用信息"""
    themeInfo = {
        'tag': '#早起读书现学现卖#',
        'term': '第6期“财报与财富”专题',
        'books': ['《用生活常识读懂财务报表》', '《轻松读懂财报》', '《五大关键数字力》', '《穿透财报》', '《证券分析》'],
        'tips': '（回答问题时请注意复制作业的以上内容，不要自行删除，否则你的作业不会被程序纳入统计）',
        'wordsNumRequired': 2
    }

    pathInfo = {
        'inputsPath': 'inputs\\',
        'outputsPath': 'outputs\\',
    }

    imgInfo = {
        'filetype': 'png'
    }

    ThreadInfo = {
        'mutex': threading.Lock(), # 创建线程锁
        'threadMaxnum': threading.Semaphore(4)  # 限制线程的最大数量
    }