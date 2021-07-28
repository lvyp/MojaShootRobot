# -*- coding: utf-8 -*-
# @Time : 2021/6/11 10:12
# @Author :
# @Site : Beijing
# @File : actionControlMode.py
# @Software: PyCharm

import threading
import globalVariable
from loggerMode import logger


def actionControlMode():
    # 动作控制模块功能实现：与底层硬件（电机）通过串口通信，发送动作控制指令
    logger.info("动作控制模块入口")
    event = globalVariable.get_event()
    rLock = threading.RLock()
    while 1:
        # logger.info("线程：" + threading.current_thread().name + " Id:" + str(threading.get_ident()))
        event.wait()
        rLock.acquire()
        if globalVariable.get_value("actionFlag") is True:
            logger.info("动作模块向底层发送数据")
            globalVariable.set_value("actionFlag", False)
        else:
            # logger.info("什么都不做")
            pass
        rLock.release()
        event.clear()
