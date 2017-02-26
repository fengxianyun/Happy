# coding:utf-8
'''
Created on 2017年2月20日

@author: raytine
'''
content = [(4, "'''"), (6, '.'), (8, 'para:')]
result = map(lambda x:x[0]*' '+x[1], content)
print '\n'.join(result)