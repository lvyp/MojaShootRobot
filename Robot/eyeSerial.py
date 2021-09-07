# -*- coding: utf-8 -*-
# @Time : 2021/9/6 19:41
# @Author :
# @Site : Beijing
# @File : eyeSerial.py
# @Software: PyCharm
import binascii
import queue
import time
import serial

from buttonTcpServer import *


class EyeSerial(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.serialLeftFd = 0
        self.serialRightFd = 0
        self.getAbailableSerialList()

    def __new__(cls, *args, **kwargs):
        if not hasattr(EyeSerial, "_instance"):
            with EyeSerial._instance_lock:
                if not hasattr(EyeSerial, "_instance"):
                    EyeSerial._instance = object.__new__(cls)
        return EyeSerial._instance

    def getAbailableSerialList(self):
        self.serialLeftFd = serial.Serial("COM15", 115200, timeout=60)
        self.serialRightFd = serial.Serial("COM14", 115200, timeout=60)
        time.sleep(0.01)

    def sendMessage(self, leftData, rightData):
        leftData = binascii.a2b_hex("5AA5078200845A01" + leftData)
        rightData = binascii.a2b_hex("5AA5078200845A01" + rightData)
        self.serialLeftFd.write(leftData)
        self.serialRightFd.write(rightData)


def eye_thread(que):
    logger.info("眼睛屏幕模块")
    while 1:
        eye = globalVariable.queEye.get()
        que.put(eye)


if __name__ == '__main__':
    # 黑屏  00 00
    # 数字0 00 01
    # 数字1 00 02
    # 数字5 00 03
    # 眨眼  00 04
    # 5分  00 36
    # 10分 00 9B
    # 睡觉  01 25
    # 睁眼  01 56
    left = "0125"
    right = "0125"
    myserial = EyeSerial()
    myserial.sendMessage(left, right)
