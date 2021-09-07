# -*- coding: utf-8 -*-
# @Time : 2021/8/5 10:54
# @Author :
# @Site : Beijing
# @File : loraSerialClass.py
# @Software: PyCharm
import binascii
import json
import threading
import time

import serial
import globalVariable
from MoJaTimer import timerMachine
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

from actionMode import que_emotion
from loggerMode import logger
from playVideoByPyGame import queBgm, queAccompany


def recvStringDeal(serStr):
    if serStr.count("}") > 1:
        nPos = serStr.find("{")
        serStr = serStr[nPos:]
        serStrList = serStr.split("}")
        return serStrList[-1]
    else:
        return serStr


class LoraSerial(object):

    _instance_lock = threading.Lock()

    def __init__(self):
        self.serialFd = serial.Serial("COM7", 9600)
        self.initTime = 0
        self.master = modbus_rtu.RtuMaster(self.serialFd)
        self.master.set_timeout(0.2)
        self.startFlag = False

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
            time.sleep(0.005)
        except Exception as e:
            # print(e)
            while True:
                globalVariable.loraErrorNumber += 1
                if globalVariable.loraErrorNumber == 3:
                    globalVariable.loraErrorNumber = 0
                    break
                else:
                    globalVariable.loraSerial.modbusRtuSendMessage(score)
            logger.info("积分器通信异常>" + str(e))

    def ledSendMessage(self, message):
        try:
            # message = globalVariable.ledQueue.get()
            print("积分器LED message>" + str(message))
            self.serialFd.write(message)
            time.sleep(0.1)
        except Exception as e:
            # print(e)
            logger.info("积分器LED通信异常>" + str(e))

    def loraRecvMessage(self):
        if self.serialFd.in_waiting:
            serStr = str(self.serialFd.read(self.serialFd.in_waiting))
            serStr = serStr.replace("b'", "").replace("'", "")
            print("loraRecvMessage>" + serStr)
            globalVariable.m_str = globalVariable.m_str + serStr
            if globalVariable.loraRecvFlag["startFlag"] is False:
                if "{" in globalVariable.m_str:
                    globalVariable.loraRecvFlag["startFlag"] = True
                else:
                    globalVariable.loraRecvFlag["startFlag"] = False
                    globalVariable.m_str = ""
                if "}" in globalVariable.m_str:
                    globalVariable.loraRecvFlag["endFlag"] = True
                else:
                    globalVariable.loraRecvFlag["endFlag"] = False
            else:
                if "}" in globalVariable.m_str:
                    globalVariable.loraRecvFlag["endFlag"] = True
                    if "type" not in globalVariable.m_str or "value" not in globalVariable.m_str:
                        globalVariable.m_str = ""
                else:
                    globalVariable.loraRecvFlag["endFlag"] = False


            print(">>>>>>" + globalVariable.m_str)

            if "}" in globalVariable.m_str and "{" in globalVariable.m_str:
                globalVariable.m_str = recvStringDeal(globalVariable.m_str)
                data = json.loads(globalVariable.m_str)
                globalVariable.m_str = ""
                globalVariable.loraRecvFlag["startFlag"] = False
                globalVariable.loraRecvFlag["endFlag"] = False
                # print(data)
                currentTime = timerMachine()
                # if data["value"] == "on":
                if data["value"] == "start":
                    # 开始游戏按钮有效效
                    self.startFlag = True
                elif data["value"] == "off":
                    print("游戏结束！！")
                    # 播放结束音效
                    if globalVariable.blueScore >= 10:
                        globalVariable.talk_1 = "./tts/start_end_music/game_end_high_score.wav"
                    else:
                        globalVariable.talk_1 = "./tts/start_end_music/game_end.wav"
                    queBgm.put(globalVariable.talk_1)
                    globalVariable.playFlag = True
                    globalVariable.set_value("scoreFlag", False)
                    globalVariable.set_value("first_start", False)
                    # 将底盘运动速度降低
                    globalVariable.mojaSerial.modifyMaxVel("0.3")
                    # 表情
                    globalVariable.m_express["expression"] = "init"
                    # quetalk.put("./tts/HuVideo_Wav/竹小剑2rl.wav")
                    # 让机器人回到初始位置进行两点运动
                    globalVariable.set_position_name_by_serial(globalVariable.mojaSerial.get_init_target_list())
                    globalVariable.set_value("mapRouteSettingFlag", False)
                    globalVariable.set_value("positionInformationFromChassisFlag", False)
                    globalVariable.set_value("mapRouteSettingInitPointFlag", True)
                    globalVariable.set_value("positionInformationFromChassisInitPointFlag", False)
                    # 游戏结束，得分状态清空
                    globalVariable.lastScore = 0
                    globalVariable.redScore = 0
                    globalVariable.yellowScore = 0
                    globalVariable.blueScore = 0
                    # 播报次数设置为初始值：0
                    globalVariable.simple_count = 0
                    globalVariable.easy_count = 0
                    globalVariable.hard_count = 0
                    # 初始时间设置为0
                    globalVariable.initTime = 0
                    # 进程间同步变量清零
                    globalVariable.syn.value = 0

                    globalVariable.currentPosNum = 0
                    # 游戏结束，计时清零
                    self.initTime = 0
                    # 开始游戏按钮无效
                    self.startFlag = False
                    # 变成初始表情
                    que_emotion.put("init")
                    # 关闭背景音乐
                    queAccompany.put("stop_music")
                    # 眼睛屏幕睡觉
                    globalVariable.queEye.put("sleep")
                elif data["value"] == "on":
                    if 0:
                        if self.startFlag:
                            if self.initTime == 0:
                                self.initTime = currentTime
                            else:
                                pass
                            # 240为游戏时长，单位秒
                            if (currentTime - self.initTime) > 180:
                                self.initTime = currentTime
                            elif currentTime - self.initTime == 0:
                                print("初次按钮触发")

                            else:
                                print("该时间段按钮触发无效")

                            if currentTime - self.initTime == 0:
                                # 播放开始音效
                                globalVariable.talk_1 = "./tts/start_end_music/game_start.wav"
                                queBgm.put(globalVariable.talk_1)
                                # 播放背景音乐
                                # queAccompanyProcess.put("./tts/bgm/BGM.wav")
                                queAccompany.put("./tts/bgm/BGM.wav")
                                globalVariable.playFlag = True
                                globalVariable.set_position_name_by_serial(globalVariable.mojaSerial.get_target_list())
                                globalVariable.currentPosNum = 0
                                globalVariable.syn.value = 0
                                # globalVariable.set_position_name_by_serial(globalVariable.mojaSerial.get_init_target_list())
                                globalVariable.set_value("mapRouteSettingInitPointFlag", False)
                                globalVariable.set_value("mapRouteSettingFlag", True)
                                globalVariable.set_value("positionInformationFromChassisFlag", False)
                                globalVariable.set_value("positionInformationFromChassisInitPointFlag", False)
                                globalVariable.set_value("scoreFlag", True)
                                globalVariable.set_value("first_start", True)
                                print("开启")
                        else:
                            pass
                    else:
                        if self.initTime == 0:
                            self.initTime = currentTime
                        else:
                            pass
                        # 240为游戏时长，单位秒
                        if (currentTime - self.initTime) > 180:
                            self.initTime = currentTime
                        elif currentTime - self.initTime == 0:
                            print("初次按钮触发")

                        else:
                            print("该时间段按钮触发无效")

                        if currentTime - self.initTime == 0:
                            # 播放开始音效
                            globalVariable.talk_1 = "./tts/start_end_music/game_start.wav"
                            queBgm.put(globalVariable.talk_1)
                            # 播放背景音乐
                            # queAccompanyProcess.put("./tts/bgm/BGM.wav")
                            queAccompany.put("./tts/bgm/BGM.wav")
                            globalVariable.playFlag = True
                            globalVariable.set_position_name_by_serial(globalVariable.mojaSerial.get_target_list())
                            globalVariable.currentPosNum = 0
                            globalVariable.syn.value = 0
                            # globalVariable.set_position_name_by_serial(globalVariable.mojaSerial.get_init_target_list())
                            globalVariable.set_value("mapRouteSettingInitPointFlag", False)
                            globalVariable.set_value("mapRouteSettingFlag", True)
                            globalVariable.set_value("positionInformationFromChassisFlag", False)
                            globalVariable.set_value("positionInformationFromChassisInitPointFlag", False)
                            globalVariable.set_value("scoreFlag", True)
                            globalVariable.set_value("first_start", True)
                            print("开启")
                else:
                    pass
                # data = {}
            else:
                pass
            # serStr = ""
        else:
            pass


# def flashing():
#     ledQueue.put(binascii.a2b_hex("A50600A0FF0000EE5A"))
#     globalVariable.loraSerial.loraRecvMessage()
#     time.sleep(1)
#     ledQueue.put(binascii.a2b_hex("A50600A0000000EE5A"))
#     time.sleep(1)
    # pass


if __name__ == "__main__":
    # globalVariable._init()
    lora = LoraSerial()
    lora.ledSendMessage(binascii.a2b_hex("A50600A0FF0000EE5A"))
    lora.ledSendMessage(binascii.a2b_hex("A50600A0000000EE5A"))
    # lora.loraRecvMessage()
    # led = threading.Thread(target=lora.ledSendMessage)
    # led.start()
    # T = threading.Thread(target=flashing)
    # T.start()

