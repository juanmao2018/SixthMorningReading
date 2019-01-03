#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2018-12-01

import os


class GetInputs(object):
    """获取inputs的文件内容存储在列表中，每个文件的内容为列表的一个元素"""
    @staticmethod
    def get_inputs(filesDir:str) -> 'list of str':
        """获取文件夹中文件的文件内容，每个文件内容以str存入List，返回List"""
        inputsLst = []
        for dirpath, dirnames, filenames in os.walk(filesDir):
            for filename in filenames:
                # print(os.path.join(filesDir,filename))
                with open(os.path.join(filesDir,filename), encoding='UTF-8') as fhand:
                    inputsLst.append(fhand.read())
        return inputsLst