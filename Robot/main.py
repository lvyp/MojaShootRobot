# -*- coding: utf-8 -*-
# @Time : 2021/6/11 10:12
# @Author :yunPeng lv
# @Site : Beijing
# @File : main.py
# @Software: PyCharm
import threading
import time
import multiprocessing
from multiprocessing import Queue

from actionMode import action_process, emo_thread, que_emotion
from eyeSerial import eye_thread, EyeSerial
from loggerMode import logger
from mapRouteSettingMode import mapRouteSettingMode
from playBGM import play_accompany_process, queAccompanyProcess
from playVideoByPyGame import play_talk, play_bgm, play_accompany
from positionInformationFromChassisMode import positionInformationFromChassisMode
from scoreMode import scoreMode
import globalVariable
from sensorCountMode import SensorCount
from tcpClient import tcpWeb
from MoJaTimer import timerMachine
from music_test import music_main


def sensorCount(score):
    sensorLock = threading.RLock()
    sensor = SensorCount()
    while 1:
        sensorLock.acquire()
        # 进行计数通信
        scoreFlag = sensor.getPortVal()
        # print("进行计数通信")
        if scoreFlag:
            score.value = score.value + 1
            print(str(score.value))
            time.sleep(0.2)
        else:
            # time.sleep(0.002)
            pass
        sensorLock.release()

def loraSerial():
    loraLock = threading.RLock()
    while 1:
        try:
            loraLock.acquire()
            globalVariable.loraSerial.loraRecvMessage()
            loraLock.release()
        except Exception as e:
            print("Main loraSerial >> " + str(e))


def serverMode():
    while 1:
        globalVariable.shootRobotServer.recvMessage()

motor18_dist = {"id": 18, "degree":0}

def getAngle(que):
    # canMotor = globalVariable.get_canMotor()
    # canMotor = CanMotor()
    # canMotor.RUN_CAN()
    # canMotor.MOTOR_INIT(18)
    angleLock = threading.RLock()
    lastAngle = 0
    lastTime = 0
    initFlag = True

    while 1:
        try:
            angleLock.acquire()
            if globalVariable.get_value("scoreFlag"):
                globalVariable.mojaSerial.getPose()
                # globalVariable.mojaSerial.recvMessage()
                currentTime = timerMachine()
                if lastTime == 0:
                    lastTime = currentTime
                elif currentTime - lastTime > 0.2:
                    lastTime = 0
                    # lastAngle = float(lastAngle)
                    globalVariable.angle = float(globalVariable.angle)
                    if abs(float(lastAngle - globalVariable.angle)) > 5.0 and abs(float(globalVariable.angle)) <= 90.0:
                        print("globalVariable.angle = ",globalVariable.angle)
                        lastAngle = float(globalVariable.angle)
                        # print("abs globalVariable.angle = ", abs(float(lastAngle - globalVariable.angle)))
                        motor18_dist["degree"] = float(globalVariable.angle) * (-1)
                        que.put(motor18_dist)
                    else:
                        pass
                else:
                    pass
            else:
                # print("lastAngle>" + str(lastAngle))
                if initFlag is True or lastAngle != 0:
                    motor18_dist["degree"] = 0
                    que.put(motor18_dist)
                    initFlag = False
                    lastAngle = 0
                else:
                    pass
        except Exception as e:
            print("Main getAngle >> " + str(e))
        finally:
            angleLock.release()


def eye_process(que_eye):
    myserial = EyeSerial()
    while True:
        eye = que_eye.get()

        if eye == "sleep":
            # print("eye>" + eye)
            myserial.sendMessage("0125", "0125")
        elif eye == "wakeUp":
            myserial.sendMessage("0156", "0156")
        elif eye == "five":
            myserial.sendMessage("0003", "0001")
            time.sleep(3)
            myserial.sendMessage("0036", "0036")
        elif eye == "fiveUp":
            myserial.sendMessage("0036", "0036")
        elif eye == "ten":
            myserial.sendMessage("0001", "0002")
            time.sleep(3)
            myserial.sendMessage("009B", "009B")
        elif eye == "tenUp":
            myserial.sendMessage("009B", "009B")
        else:
            pass


if __name__ == '__main__':
    try:
        # 墨甲导览机器人启动入口
        logger.info("墨甲射击机器人启动入口")
        que_action = Queue(18)
        music_main(que_action)
        globalVariable._init()

        # 进程间共享全局变量
        globalVariable.syn = multiprocessing.Value("i", 0)
        # 为传感器创建单独进程，防止资源被强占
        sensorProcess = multiprocessing.Process(target=sensorCount, args=(globalVariable.syn, ))
        sensorProcess.start()

        # 进程间共享全局变量
        globalVariable.m_express = multiprocessing.Manager().dict()
        # 为表情创建单独进程，防止资源被抢占
        expressionProcess = multiprocessing.Process(target=action_process, args=(que_action, ))
        expressionProcess.start()

        # 背景音乐进程
        que_accompany = Queue(18)
        accompanyProcess = multiprocessing.Process(target=play_accompany_process, args=(que_accompany,))
        accompanyProcess.start()

        # 眼睛控制线程
        que_eye = Queue(1)
        eyeProcess = multiprocessing.Process(target=eye_process, args=(que_eye,))
        eyeProcess.start()

        #设置表情初始化
        # action(globalVariable.get_comMotor(), globalVariable.get_canMotor(), "init")
        # globalVariable.m_express["expression"] = "init"
        globalVariable.set_value("init_plot", False)
        globalVariable.set_value("first_start", False)
        globalVariable.set_value("scoreFlag", False)
        globalVariable.set_value("actionFlag", False)
        globalVariable.set_value("mapRouteSettingFlag", False)
        globalVariable.set_value("mapRouteSettingInitPointFlag", True)
        globalVariable.set_value("positionInformationFromChassisFlag", False)
        globalVariable.set_value("positionInformationFromChassisInitPointFlag", False)

        globalVariable.set_position_name_by_serial(globalVariable.mojaSerial.get_init_target_list())
        # 将底盘运动速度降低
        globalVariable.mojaSerial.modifyMaxVel("0.3")
        globalVariable.set_value("mapRouteSettingFlag", False)
        globalVariable.set_value("positionInformationFromChassisFlag", False)
        globalVariable.set_value("mapRouteSettingInitPointFlag", True)
        globalVariable.set_value("positionInformationFromChassisInitPointFlag", False)

        # 设置线程组
        threads = []

        # 创建线程：
        lora = threading.Thread(target=loraSerial)
        score = threading.Thread(target=scoreMode)
        # tcpServer = threading.Thread(target=serverMode)
        emotion = threading.Thread(target=emo_thread, args=(que_emotion, que_action))
        mapRouteSetting = threading.Thread(target=mapRouteSettingMode)
        positionInformationFromChassis = threading.Thread(target=positionInformationFromChassisMode)
        tcpClient = threading.Thread(target=tcpWeb)
        angle = threading.Thread(target=getAngle, args=(que_action, ))


        #音频播放线程
        thread_play = threading.Thread(target=play_talk)
        thread_bgm = threading.Thread(target=play_bgm)
        thread_accompany = threading.Thread(target=play_accompany, args=(que_accompany,))

        # 眼睛屏幕控制线程
        thread_eye = threading.Thread(target=eye_thread, args=(que_eye,))


        lora.setName("lora")
        score.setName("score")
        tcpClient.setName("tcpClient")
        mapRouteSetting.setName("mapRouteSetting")
        positionInformationFromChassis.setName("positionInformationFromChassis")
        angle.setName("angle")
        thread_play.setName("playVideo")
        thread_bgm.setName("playBgm")
        thread_accompany.setName("thread_accompany")
        thread_eye.setName("eye")


        # 添加到线程组
        threads.append(emotion)
        threads.append(lora)
        threads.append(score)
        # threads.append(tcpClient)
        threads.append(mapRouteSetting)
        threads.append(positionInformationFromChassis)
        threads.append(angle)
        threads.append(thread_play)
        threads.append(thread_bgm)
        threads.append(thread_accompany)
        threads.append(thread_eye)

        # 开启线程
        for thread in threads:
            thread.start()

        # 眼睛屏幕睡觉
        globalVariable.queEye.put("sleep")

        # 线程阻塞
        for thread in threads:
            thread.join()


    except Exception as e:
        print("exit error >>" + str(e))
