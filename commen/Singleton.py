#coding:utf-8
'''
Created on 2017年2月19日

@author: raytine
'''
def singleton(cls, *args, **kw):
    instance = {}
    def _singleton():
        if cls not in instance:
            instance[cls] = cls(*args, **kw)
        return instance[cls]
    return _singleton