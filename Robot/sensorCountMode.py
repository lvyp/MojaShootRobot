# -*- coding: utf-8 -*-
# @Time : 2021/8/5 15:04
# @Author :
# @Site : Beijing
# @File : sensorCountMode.py
# @Software: PyCharm
import ctypes
import threading


class SensorCount(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.count = 0
        # 用于定于读取GPI状态的变量
        self.ReadValue_Gpi1 = ctypes.c_ulong()
        self.ReadValue_Gpi7 = ctypes.c_ulong()
        self.GetPortVal = 0
        self.SetPortVal = 0
        self.createSerial()

    def __new__(cls, *args, **kwargs):
        if not hasattr(SensorCount, "_instance"):
            with SensorCount._instance_lock:
                if not hasattr(SensorCount, "_instance"):
                    SensorCount._instance = object.__new__(cls)
        return SensorCount._instance

    def createSerial(self):
        stdCall = ctypes.WinDLL("./WinIo64.dll")
        InitializeWinIo = stdCall.InitializeWinIo
        InitializeWinIo.restype = ctypes.c_bool

        bComplete = InitializeWinIo()
        if not bComplete:
            print("InitializeWinIo Fail!\r\n01.请检查Python环境是32位还是64位,"
                  "如果是32位则需要引入32位的dll文件.\r\n02.请检查WinIo64.dll和WinIo32.dll是否和Python脚本在同一个目录下.\r\n")
            quit()
        else:
            print("InitializeWinIo Ok!")
            self.GetPortVal = stdCall.GetPortVal
            self.GetPortVal.restype = ctypes.c_bool
            self.GetPortVal.argtypes = [ctypes.c_ushort, ctypes.POINTER(ctypes.c_ulong), ctypes.c_ubyte]
            self.SetPortVal = stdCall.SetPortVal
            self.SetPortVal.restype = ctypes.c_bool
            self.SetPortVal.argtypes = [ctypes.c_ushort, ctypes.c_ulong, ctypes.c_ubyte]

    def getPortVal(self):
        returnValue = False
        self.GetPortVal(0xA00, self.ReadValue_Gpi1, 1)
        self.GetPortVal(0xA04, self.ReadValue_Gpi7, 1)
        # print("GPI1>" + str(self.ReadValue_Gpi1.value))
        # print("GPI7>" + str(self.ReadValue_Gpi7.value))
        # Gpi1或Gpi7有一个传感器返回0，即得分
        if (int(self.ReadValue_Gpi7.value) & 0x08 == 0) or \
                (int(self.ReadValue_Gpi1.value) & 0x01 == 0):
            returnValue = True
        return returnValue
