# coding: utf-8
'''
Created on 2017年2月22日

@author: wczhang.fxy
'''
from CommenFileDeal import makeChangeInEveryFile
from MyLogging import Log
import re
import traceback

log = Log('comment_add_log.txt')


def addComment(path):
    log.info('开始为{}增加注释'.format(path))
    indent_length = {}
    content = []
    result = []
    add_content = {}
    with open(path, 'r') as fp:
        temp_name = ''
        temp_indent = 0
        for line in fp:
            try:
                content.append(line)
                if 'def' in line:
                    log.info('检测到函数')
                    temp_indent = len(re.findall('([ ]*)def', line)[0])
                    temp_name = re.findall('def([a-zA-Z0-9_ ]*)\(', line)[0].strip()
                    indent_length[temp_name] = temp_indent
                    para = re.findall('\(([a-zA-Z0-9=_,\* \'"]*)\)', line)[0].split(',')
                    para = map(lambda x: x.strip(), para)
                    log.info('函数名为:{},缩进为:{},参数为:{}'.format(temp_name, temp_indent, para))
                    add_message = addContent('def', temp_indent, para)
                    add_content[temp_name] = add_message
                if 'return' in line:
                    log.info('检测到返回')
                    para = re.findall('return ([a-zA-Z0-9=_,\* \'"]*)', line)[0].split(',')
                    para = map(lambda x: x.strip(), para)
                    log.info('函数名为:{},缩进为:{},参数为:{}'.format(temp_name, temp_indent, para))
                    add_message = addContent('return', temp_indent, para)
                    add_content[temp_name] += add_message
            except IndexError:
                log.warning('源代码解析错误，可能出现不为关键子的def或return字符串， 暂时忽略，{}'.format(traceback.format_exc()))
    for line in content:
        result.append(line)
        if 'def' in line:
            try:
                temp_name = re.findall('def([a-zA-Z0-9_ ]*)\(', line)[0].strip()
                result.append(add_content[temp_name])
            except IndexError:
                log.warning('源代码解析错误，可能出现不为关键子的def或return字符串， 暂时忽略，{}'.format(traceback.format_exc()))
    log.info('添加注释完成')
    return ''.join(result)


def addContent(name, indent, para):
    if name == 'def':
        content = [(indent, "'''"), (indent, '.'), (indent, 'para:')]
        for line in para:
            content.append((indent+4, line+':'))
            content.append((indent+8, 'type:'))
            content.append((indent+8, 'content:'))
        content.append((indent, ''))
    if name == 'return':
        content = [(indent, 'return:')]
        for line in para:
            content.append((indent+4, line+':'))
            content.append((indent+8, 'type:'))
            content.append((indent+8, 'content:'))
        content.append((indent, "'''"))
        content.append((indent, ""))
    result = '\n'.join(map(lambda x:x[0]*' '+x[1], content))
    return result

if __name__ == '__main__':
    print addComment('D:/eclipse-java-mars-2-win32-x86_64/workspace/FlowPredict/predict_1.py')