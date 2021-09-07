import binascii
import os
import queue
import time
import pygame
import threading
import globalVariable
from MoJaTimer import timerMachine

#4、#初始化
from loggerMode import logger

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

#事件同步
eventPyGame = threading.Event()
queBgm = queue.Queue(10)
quetalk = queue.Queue(1)
queAccompany = queue.Queue(1)
start_end = ["./tts/start_end_music/game_start.wav", "./tts/start_end_music/game_end.wav"]
sound = pygame.mixer.Sound("./tts/start_end_music/game_start.wav")  # 播放
soundAccompany = pygame.mixer.Sound("./tts/bgm/BGM.wav")  # 播放

m_list = ["./tts/HuVideo_Wav/竹小剑6rl", "./tts/HuVideo_Wav/竹小剑7rl"]

def stop_thread():
    # print(">>>>>>>>>>>>>>stop_thread")
    fistPlay = 0
    while 1:
        """线程运行函数"""
        currentTime = timerMachine()

        if globalVariable.playFlag and ((currentTime - fistPlay >= 1)):
            # print(globalVariable.talk_1)
            if fistPlay == 0:
                fistPlay = currentTime
            else:
                fistPlay = 0
            if globalVariable.talk_1 not in start_end and globalVariable.talk_1 != "./tts/HuVideo_Wav/shootIn.wav":
                eventPyGame.set()  # 计数器获得锁
            # else:
            #     queBgm.put(globalVariable.talk_1)
            # play.release()
            globalVariable.playFlag = False
        else:
            globalVariable.playFlag = False


def startEndFlashing():
    globalVariable.loraSerial.ledSendMessage(binascii.a2b_hex("A50600A0FF0000EE5A"))
    # 机器人LED
    globalVariable.robotLed.ledSendMessage(binascii.a2b_hex("A50600A0FF0000EE5A"))

    globalVariable.loraSerial.ledSendMessage(binascii.a2b_hex("A50600A000FF00EE5A"))
    # 机器人LED
    globalVariable.robotLed.ledSendMessage(binascii.a2b_hex("A50600A000FF00EE5A"))

    globalVariable.loraSerial.ledSendMessage(binascii.a2b_hex("A50600A00000FFEE5A"))
    # 机器人LED
    globalVariable.robotLed.ledSendMessage(binascii.a2b_hex("A50600A00000FFEE5A"))

    globalVariable.loraSerial.ledSendMessage(binascii.a2b_hex("A50600A0000000EE5A"))
    # 机器人LED
    globalVariable.robotLed.ledSendMessage(binascii.a2b_hex("A50600A0000000EE5A"))
    # time.sleep(0.1)
    globalVariable.loraSerial.ledSendMessage(binascii.a2b_hex("A50600A0FF0000EE5A"))
    # 机器人LED
    globalVariable.robotLed.ledSendMessage(binascii.a2b_hex("A50600A0FF0000EE5A"))

    globalVariable.loraSerial.ledSendMessage(binascii.a2b_hex("A50600A000FF00EE5A"))
    # 机器人LED
    globalVariable.robotLed.ledSendMessage(binascii.a2b_hex("A50600A000FF00EE5A"))

    globalVariable.loraSerial.ledSendMessage(binascii.a2b_hex("A50600A00000FFEE5A"))
    # 机器人LED
    globalVariable.robotLed.ledSendMessage(binascii.a2b_hex("A50600A00000FFEE5A"))

    globalVariable.loraSerial.ledSendMessage(binascii.a2b_hex("A50600A0000000EE5A"))
    # 机器人LED
    globalVariable.robotLed.ledSendMessage(binascii.a2b_hex("A50600A0000000EE5A"))
    # time.sleep(0.1)
    globalVariable.loraSerial.ledSendMessage(binascii.a2b_hex("A50600A0FF0000EE5A"))
    # 机器人LED
    globalVariable.robotLed.ledSendMessage(binascii.a2b_hex("A50600A0FF0000EE5A"))

    globalVariable.loraSerial.ledSendMessage(binascii.a2b_hex("A50600A000FF00EE5A"))
    # 机器人LED
    globalVariable.robotLed.ledSendMessage(binascii.a2b_hex("A50600A000FF00EE5A"))

    globalVariable.loraSerial.ledSendMessage(binascii.a2b_hex("A50600A00000FFEE5A"))
    # 机器人LED
    globalVariable.robotLed.ledSendMessage(binascii.a2b_hex("A50600A00000FFEE5A"))

    globalVariable.loraSerial.ledSendMessage(binascii.a2b_hex("A50600A0000000EE5A"))
    # 机器人LED
    globalVariable.robotLed.ledSendMessage(binascii.a2b_hex("A50600A0000000EE5A"))


def shootFlashing():
    globalVariable.loraSerial.ledSendMessage(binascii.a2b_hex("A50600A0FF0000EE5A"))
    # 机器人LED
    globalVariable.robotLed.ledSendMessage(binascii.a2b_hex("A50600A0FF0000EE5A"))

    globalVariable.loraSerial.ledSendMessage(binascii.a2b_hex("A50600A000FF00EE5A"))
    # 机器人LED
    globalVariable.robotLed.ledSendMessage(binascii.a2b_hex("A50600A000FF00EE5A"))

    globalVariable.loraSerial.ledSendMessage(binascii.a2b_hex("A50600A00000FFEE5A"))
    # 机器人LED
    globalVariable.robotLed.ledSendMessage(binascii.a2b_hex("A50600A00000FFEE5A"))

    globalVariable.loraSerial.ledSendMessage(binascii.a2b_hex("A50600A0000000EE5A"))
    # 机器人LED
    globalVariable.robotLed.ledSendMessage(binascii.a2b_hex("A50600A0000000EE5A"))
    # time.sleep(0.1)
    globalVariable.loraSerial.ledSendMessage(binascii.a2b_hex("A50600A0FF0000EE5A"))
    # 机器人LED
    globalVariable.robotLed.ledSendMessage(binascii.a2b_hex("A50600A0FF0000EE5A"))

    globalVariable.loraSerial.ledSendMessage(binascii.a2b_hex("A50600A000FF00EE5A"))
    # 机器人LED
    globalVariable.robotLed.ledSendMessage(binascii.a2b_hex("A50600A000FF00EE5A"))

    globalVariable.loraSerial.ledSendMessage(binascii.a2b_hex("A50600A00000FFEE5A"))
    # 机器人LED
    globalVariable.robotLed.ledSendMessage(binascii.a2b_hex("A50600A00000FFEE5A"))

    globalVariable.loraSerial.ledSendMessage(binascii.a2b_hex("A50600A0000000EE5A"))
    # # 机器人LED
    globalVariable.robotLed.ledSendMessage(binascii.a2b_hex("A50600A0000000EE5A"))
    # globalVariable.ledQueue.put(binascii.a2b_hex("A50600A0FF0000EE5A"))
    # globalVariable.loraSerial.loraRecvMessage()
    # time.sleep(1)
    # globalVariable.ledQueue.put(binascii.a2b_hex("A50600A0000000EE5A"))
    # time.sleep(1)


def play_close():
    soundAccompany.stop()


def play_accompany(que):
    logger.info("背景音播放模块")
    while 1:
        file = queAccompany.get()
        if os.path.isfile(file):

            print(file)
            if 0:
                soundAccompany.__init__(file)
                soundAccompany.set_volume(0.7)  # 设置声音
                soundAccompany.play(loops=100)  # 播放音乐
            else:
                que.put(file)
        else:
            que.put(file)


def play_bgm():
    # print(">>>>>>>>>>>>>>play_bgm")
    while 1:
        file = queBgm.get()
        print(file)
        # sound = pygame.mixer.Sound(file)  # 播放
        if os.path.isfile(file):
            sound.__init__(file)
            sound.set_volume(1)  # 设置声音
            sound.play()  # 播放音乐
        else:
            pass

        if globalVariable.get_value("scoreFlag"):
            # globalVariable.loraSerial.modbusRtuSendMessage(globalVariable.blueScore)
            if globalVariable.blueScore == 0:
                startEndFlashing()
            else:
                # if globalVariable.blueScore >= 18:
                #     globalVariable.blueScore = 0
                shootFlashing()
        else:
            startEndFlashing()
            pass


def play_talk():
    fistPlay = 0
    lastFile = ""
    while 1:
        file = quetalk.get()
        currentTime = timerMachine()
        # print("", file, currentTime, fistPlay)
        if lastFile in m_list and file not in m_list:
            difference = 6
        else:
            difference = currentTime - fistPlay
        if os.path.isfile(file) and (difference >= 5):
            fistPlay = currentTime
            # print(file)
            pygame.mixer.music.load(file)
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play()
            lastFile = file
        else:
            pass
        # eventPyGame.wait()
        # pygame.mixer.music.load(globalVariable.talk_1)
        # pygame.mixer.music.set_volume(0.5)
        # pygame.mixer.music.play()
        # eventPyGame.clear()
        # if globalVariable.talk_1 in start_end:
        #     time.sleep(3)
        # if globalVariable.talk_1 == "./tts/HuVideo_Wav/shootIn.wav":
        #     time.sleep(1)
        # print("play")
        # sem.release()
        # event.wait()
        # event.clear()
        # pygame.mixer.music.stop()


if __name__ == '__main__':
    globalVariable._init()
    # 创建线程
    # thread_hi = threading.Thread(target=test_thread)
    thread_stop = threading.Thread(target=stop_thread)
    thread_play = threading.Thread(target=play_talk)
    # 启动线程
    # thread_hi.start()
    thread_stop.start()
    thread_play.start()

    globalVariable.playFlag = True
    time.sleep(5)
    globalVariable.playFlag = True
    time.sleep(6)
    globalVariable.playFlag = True
    time.sleep(11)
    globalVariable.playFlag = True

