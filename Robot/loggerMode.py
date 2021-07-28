# -*- coding: utf-8 -*-
# @Time : 2021/6/11 10:12
# @Author :
# @Site : Beijing
# @File : loggerMode.py
# @Software: PyCharm

import os
import logging.handlers
import datetime

# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关  此时是INFO

# 第二步，创建一个handler，用于写入日志文件

# 判断路径是否存在
path = str(datetime.date.today())
isExists = os.path.exists(path)
# 判断结果
if not isExists:
    # 如果不存在则创建目录
    # 创建目录操作函数
    os.makedirs(path)
    print(path + ' 创建成功')
else:
    # 如果目录存在则不创建，并提示目录已存在
    print(path + ' 目录已存在')

logfile = './' + path + '/' + path + '_log.log'
# fh = logging.FileHandler(logfile, mode='a')  # open的打开模式这里可以进行参考
fh = logging.handlers.RotatingFileHandler(logfile, maxBytes=4*1024*1024, backupCount=40)
fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关

# 第三步，再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)   # 输出到console的log等级的开关

# 第四步，定义handler的输出格式（时间，文件，行数，错误级别，错误提示）
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 第五步，将logger添加到handler里面
logger.addHandler(fh)
logger.addHandler(ch)
