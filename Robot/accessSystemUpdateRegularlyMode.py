# -*- coding: utf-8 -*-
# @Time : 2021/6/11 10:12
# @Author :
# @Site : Beijing
# @File : accessSystemUpdateRegularlyMode.py
# @Software: PyCharm
import threading
import globalVariable
from loggerMode import logger


def accessSystemUpdateRegularlyMode():
    # 定时访问系统更新模块:实际为tcp客户端,根据定时器，定期访问服务器查看是否需要版本更新
    logger.info("定时访问系统更新模块入口")
    event = globalVariable.get_event()
    rLock = threading.RLock()
    while 1:
        logger.info("线程：" + threading.current_thread().name + " Id:" + str(threading.get_ident()))
        event.wait()
        rLock.acquire()
        # 代码实现部分
        # 代码实现部分
        rLock.release()
        event.clear()
