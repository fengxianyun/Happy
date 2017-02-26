# coding:utf-8
'''
Created on 2017��1��26��

@author: a7999011
'''
import logging
from Dir import cur_file_dir
from logging.handlers import RotatingFileHandler
import os


class Log():
    def __init__(self, log_name, dir_path=cur_file_dir()):
        self.name = os.path.join(dir_path, log_name)
        # 创建一个logger
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(thread)d: %(levelname)s %(message)s")

        # 创建一个handler，用于写入日志文件
        rh = RotatingFileHandler(self.name, maxBytes=1024 * 1024 * 10, backupCount=10)
        rh.setLevel(logging.INFO)
        # 创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 定义handler的输出格式
        rh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(rh)
        self.logger.addHandler(ch)
        self.info('Log路径为:{}'.format(self.name))

    def debug(self, string):
        logging.debug(string)

    def info(self, string):
        self.logger.info(string)

    def warning(self, string):
        self.logger.warning(string)

    def error(self, string):
        self.logger.error(string)
        
if __name__ == '__main__':
    log = Log('mylog')
    log.info('lll')
