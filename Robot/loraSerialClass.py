# -*- coding: utf-8 -*-
# @Time : 2021/8/5 10:54
# @Author :
# @Site : Beijing
# @File : loraSerialClass.py
# @Software: PyCharm
import json
import threading
import serial
import globalVariable
from MoJaTimer import timerMachine
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu


class LoraSerial(object):

    _instance_lock = threading.Lock()

    def __init__(self):
        self.serialFd = serial.Serial("COM7", 9600)
        self.initTime = 0
        self.master = modbus_rtu.RtuMaster(self.serialFd)
        self.master.set_timeout(5.0)

    def __new__(cls, *args, **kwargs):
        if not hasattr(LoraSerial, "_instance"):
            with LoraSerial._instance_lock:
                if not hasattr(LoraSerial, "_instance"):
                    LoraSerial._instance = object.__new__(cls)
        return LoraSerial._instance

    def modbusRtuSendMessage(self, score):
        try:
            self.master.execute(slave=1, function_code=cst.WRITE_MULTIPLE_REGISTERS,
                                starting_address=20012, quantity_of_x=2, output_value=[score, 0])
        except Exception as e:
            print(e)

    def loraRecvMessage(self):
        if self.serialFd.in_waiting:
            serStr = str(self.serialFd.read(self.serialFd.in_waiting))
            print(">>>>>>" + serStr)
            serStr = serStr.replace("b'", "").replace("'", "")

            if serStr != "":
                data = json.loads(serStr)
                # print(data)
                currentTime = timerMachine()
                if data["value"] == "on":
                    if self.initTime == 0:
                        self.initTime = currentTime
                    else:
                        pass
                    # 240为游戏时长，单位秒
                    if (currentTime - self.initTime) > 240:
                        self.initTime = currentTime
                    elif currentTime - self.initTime == 0:
                        print("初次按钮触发")

                    else:
                        print("该时间段按钮触发无效")

                    if currentTime - self.initTime == 0:
                        globalVariable.set_position_name_by_serial(globalVariable.mojaSerial.get_target_list())
                        globalVariable.set_value("mapRouteSettingInitPointFlag", False)
                        globalVariable.set_value("mapRouteSettingFlag", True)
                        globalVariable.set_value("scoreFlag", True)
                        globalVariable.set_value("first_start", True)
                        print("开启")
                else:
                    pass
                data = {}
            else:
                pass
            serStr = ""
        else:
            pass
