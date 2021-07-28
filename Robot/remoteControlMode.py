# -*- coding: utf-8 -*-
# @Time : 2021/6/11 10:12
# @Author :
# @Site : Beijing
# @File : remoteControlMode.py
# @Software: PyCharm

import threading
import globalVariable
from loggerMode import logger


def remoteControlMode():
    # 远程控制模块：支持远程服务器发送指令，控制动作模块、双机器人互动模块以及TTS播报
    logger.info("远程控制模块入口")
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
