# coding:utf-8
'''
Created on 2017年2月19日

@author: raytine
'''
import os

def makeChangeInEveryFile(path, changeFileFunction=None, changeDirFunction=None):
    '''
    .对同一文件夹内的文件或文件夹进行修改
    para:
        path:
            content:更改路径
            type:str
        changeFileFunction:
            content:对文件修改的方法
            type:function
        changeDirFunction:
            content:对文件夹的修改方法
            type:function
    '''
    for parent,dirnames,filenames in os.walk(path):
        for dirname in  dirnames:
            if changeDirFunction!=None:
                changeDirFunction(os.path.join(path, dirname))
            makeChangeInEveryFile(os.path.join(path, dirname), changeFileFunction, changeDirFunction)
        for filename in filenames:
            if changeFileFunction!=None:
                changeFileFunction(os.path.join(parent, filename))


if __name__ == '__main__':
    path = 'C:/Users/raytine/Downloads/Weather_Date/Weather_Date'