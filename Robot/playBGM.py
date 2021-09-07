import os
import queue
import threading

import pygame
from loggerMode import logger

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

queAccompanyProcess = queue.Queue(1)

soundAccompany = pygame.mixer.Sound("./tts/bgm/BGM.wav")  # 播放


def play_close_process():
    soundAccompany.stop()


def play_accompany_process(que):
    logger.info("背景音播放模块")
    stop_bgm = threading.Thread(target=play_close_process)
    stop_bgm.start()
    while 1:
        file = que.get()
        # file = "./tts/bgm/BGM.wav"
        if os.path.isfile(file):
            print(file)
            soundAccompany.__init__(file)
            soundAccompany.set_volume(0.4)  # 设置声音
            soundAccompany.play(loops=100)  # 播放音乐
        else:
            play_close_process()


def play_talk():
    queAccompanyProcess.put("./tts/bgm/BGM.wav")


if __name__ == "__main__":
    # 创建线程
    # thread_hi = threading.Thread(target=test_thread)
    thread_stop = threading.Thread(target=play_accompany_process)
    thread_play = threading.Thread(target=play_talk)
    # 启动线程
    # thread_hi.start()
    thread_stop.start()
    thread_play.start()