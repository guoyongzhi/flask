#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.handlers
import os
import time


class logs(object):
    def __init__(self, name=None):
        """
        :rtype: object
        """
        # 清除句柄
        self.logger = logging.getLogger("")
        # print(self.logger.handlers)
        self.logger.handlers.clear()
        # 设置输出的等级
        LEVELS = {'NOSET': logging.NOTSET, 'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'WARNING': logging.WARNING,
                  'ERROR': logging.ERROR, 'CRITICAL': logging.CRITICAL}
        # 创建文件目录
        logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), r"logs2")
        if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
            pass
        else:
            os.mkdir(logs_dir)
        # 修改log保存位置
        # timestamp=time.strftime("%Y-%m-%d", time.localtime())
        logfilename = str(name) + ".log"
        logfilepath = os.path.join(logs_dir, logfilename)
        rotatingFileHandler = logging.handlers.RotatingFileHandler(filename=logfilepath, encoding='utf-8')
        # 设置输出格式
        formatter = logging.Formatter('%(asctime)s -%(levelname)s- %(message)s', '%Y-%m-%d %H:%M:%S')
        rotatingFileHandler.setFormatter(formatter)
        # if not logging.handlers:
        # 控制台句柄
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        # 添加内容到日志句柄中
        self.logger.addHandler(rotatingFileHandler)
        self.logger.addHandler(console)
        self.logger.setLevel(logging.INFO)
    
    def info(self, message):
        self.logger.info(message)
        
    def debug(self, message):
        self.logger.debug(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
