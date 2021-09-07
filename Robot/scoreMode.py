# -*- coding: utf-8 -*-
# @Time : 2021/7/29 14:01
# @Author :
# @Site : Beijing
# @File : scoreMode.py
# @Software: PyCharm
import random
import globalVariable
from actionMode import que_emotion, emotion_arr
from loggerMode import logger
import threading
from MoJaTimer import *
from music_test import queue_action_sound
from playVideoByPyGame import queBgm, quetalk, queAccompany


def robotStatus():
    # 计算总积分
    sumScore = globalVariable.blueScore

    # 得分将本次得分值赋值给上一次得分值
    lastScore = globalVariable.lastScore
    globalVariable.lastScore = sumScore

    # 计算游戏时间
    currentTime = timerMachine()
    # if globalVariable.initTime == 0:
    #     globalVariable.initTime = currentTime

    # 进球播放对话 >（优先于）表情变化
    if lastScore != sumScore:
        # 进球，不进球计时更新
        globalVariable.lastShootOutTime = timerMachine()
        # 播放打击音效
        globalVariable.talk_1 = "./tts/HuVideo_Wav/shootIn{0}.wav".format(random.randint(0, 3))
        queBgm.put(globalVariable.talk_1)
        # 表情计时时间更新
        globalVariable.initTime = currentTime
        if sumScore == 1:
            file_name = "./tts/HuVideo_Wav/竹小剑2rl.wav"
        else:
            file_name = "./tts/HuVideo_Wav/竹小剑{0}rl.wav".format(random.randint(3, 5))
        if queue_action_sound.empty() == True:
            queue_action_sound.put(file_name)
        if quetalk.empty() == True:
            quetalk.put(file_name)

        if (1 <= sumScore <= 4):
            que_emotion.put(emotion_arr[8])  # 挑衅
            # 提升底盘速度
            globalVariable.mojaSerial.modifyMaxVel("0.4")
        elif (5 <= sumScore <= 9):
            if sumScore == 5:
                globalVariable.queEye.put("five")
            else:
                globalVariable.queEye.put("fiveUp")
            que_emotion.put(emotion_arr[9])  # 惊奇
            # 提升底盘速度
            globalVariable.mojaSerial.modifyMaxVel("0.5")
        elif (10 <= sumScore <= 14):
            if sumScore == 10:
                globalVariable.queEye.put("ten")
            else:
                globalVariable.queEye.put("tenUp")
            que_emotion.put(emotion_arr[10])  # 愤怒
            # 提升底盘速度
            globalVariable.mojaSerial.modifyMaxVel("0.6")
        elif (15 <= sumScore <= 18):
            globalVariable.queEye.put("tenUp")
            que_emotion.put(emotion_arr[11])  # 尴尬
            # 提升底盘速度
            globalVariable.mojaSerial.modifyMaxVel("0.7")
        else:
            pass
    else:
        # currentTime = timerMachine()
        if currentTime - globalVariable.lastShootOutTime >= 20:
            globalVariable.lastShootOutTime = currentTime
            globalVariable.initTime = currentTime
            file_name = "./tts/HuVideo_Wav/竹小剑{0}rl.wav".format(6 + (random.randint(0, 100) % 2))
            if quetalk.empty() == True:
                quetalk.put(file_name)
            if queue_action_sound.empty() == True:
                queue_action_sound.put(file_name)
        else:
            if (sumScore == 0) and (currentTime - globalVariable.initTime > 7):
                que_emotion.put(emotion_arr[1])  # 开心
                globalVariable.initTime = currentTime

            # 表情变化 >（优先于）轮播表情
            if (sumScore >= 1) and (currentTime - globalVariable.initTime > 7):
                emotionStr = emotion_arr[random.randint(1, 5)]
                # print("不进球时轮播表情>" + emotionStr)
                que_emotion.put(emotionStr)
                globalVariable.initTime = currentTime

    # 总分高于18分结束游戏
    if sumScore >= 18:
        # 播放结束音效
        if globalVariable.blueScore >= 10:
            globalVariable.talk_1 = "./tts/start_end_music/game_end_high_score.wav"
        else:
            globalVariable.talk_1 = "./tts/start_end_music/game_end.wav"
        queBgm.put(globalVariable.talk_1)
        globalVariable.playFlag = True
        globalVariable.set_value("scoreFlag", False)
        # 将底盘运动速度降低
        globalVariable.mojaSerial.modifyMaxVel("0.3")
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
        globalVariable.lastShootOutTime = 0
        # 进程间同步变量清零
        globalVariable.syn.value = 0

        globalVariable.currentPosNum = 0

        # 按钮计时器清理
        globalVariable.loraSerial.initTime = 0

        # 开始游戏按钮无效
        globalVariable.loraSerial.startFlag = False
        # 眼睛屏幕睡觉
        globalVariable.queEye.put("sleep")
        # 变成初始表情
        que_emotion.put("init")

        # 关闭背景音乐
        queAccompany.put("stop_music")


def scoreMode():
    logger.info("得分模块入口")
    event = globalVariable.get_event()
    rLock = threading.RLock()
    lastTime = 0
    # comMotor = globalVariable.get_comMotor()
    # canMotor = globalVariable.get_canMotor()
    while 1:
        rLock.acquire()
        if globalVariable.get_value("scoreFlag"):
            # 打呼噜初始时间清零
            lastTime = 0
            # print("lastScore>" + str(globalVariable.lastScore))
            # print("blueScore>" + str(globalVariable.blueScore))
            globalVariable.blueScore = globalVariable.syn.value
            if globalVariable.get_value("first_start"):
                globalVariable.blueScore = 0
                globalVariable.loraSerial.modbusRtuSendMessage(globalVariable.blueScore)
                # 眼睛屏幕睁眼
                globalVariable.queEye.put("wakeUp")
                globalVariable.set_value("first_start", False)
            # 判断是否得分，得分通过modbus rtu控制得分牌显示得分
            if globalVariable.lastScore == globalVariable.blueScore:
                pass
            else:
                globalVariable.loraSerial.modbusRtuSendMessage(globalVariable.blueScore)

            # 机器人状态变化
            # robotStatus(comMotor, canMotor)
            robotStatus()
        else:
            currentTime = timerMachine()
            # if lastTime == 0:
            #     lastTime = currentTime
            if currentTime - lastTime >= 29:
                lastTime = currentTime
                quetalk.put("./tts/HuVideo_Wav/竹小剑1打呼噜rl.wav")
                queue_action_sound.put("./tts/HuVideo_Wav/竹小剑1打呼噜rl.wav")
                # lastTime = 0
            else:
                pass

        event.set()
        rLock.release()


if __name__ == "__main__":
    globalVariable._init()
    globalVariable.set_value("scoreFlag", False)
    scoreMode()
