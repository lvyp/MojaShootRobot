# -*- coding: utf-8 -*-
# @Time : 2021/9/4 10:09
# @Author :
# @Site : Beijing
# @File : robotLed.py
# @Software: PyCharm
import threading
import time

import serial

from loggerMode import logger


class RobotLedSerial(object):

    _instance_lock = threading.Lock()

    def __init__(self):
        self.serialFd = serial.Serial("COM3", 9600)

    def __new__(cls, *args, **kwargs):
        if not hasattr(RobotLedSerial, "_instance"):
            with RobotLedSerial._instance_lock:
                if not hasattr(RobotLedSerial, "_instance"):
                    RobotLedSerial._instance = object.__new__(cls)
        return RobotLedSerial._instance

    def ledSendMessage(self, message):
        try:
            # message = globalVariable.ledQueue.get()
            print("机器人LED message>" + str(message))
            self.serialFd.write(message)
            time.sleep(0.1)
        except Exception as e:
            # print(e)
            logger.info("机器人LED通信异常>" + str(e))