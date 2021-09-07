import time
import pygame
import threading
import wave
import contextlib
import queue
import  os

#3、设置音乐绝对路径
#睡觉
talk_sleep = r"竹小剑1打呼噜rl.wav"
#打不着
talk_defiance = r"竹小剑打不着 rl.wav"
#对话1
talk_1 = r"竹小剑2rl.wav"
#对话2
talk_2 = r"竹小剑3rl.wav"
#对话3
talk_3 = r"竹小剑4rl.wav"
#对话4
talk_4 = r"竹小剑5rl.wav"
#对话5

#4、#初始化
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

#事件同步
event = threading.Event()
play = threading.Semaphore(0)
sem = threading.Semaphore(0)
play_sound = queue.Queue()

def play_input(que):
    while 1:
        str = input("请输入")
        while 1:
            if (os.path.isfile(str)):
                que.put(str)
                play_sound.put(str)
            else:
                print("file is no-exist")
            time.sleep(10)
        time.sleep(0.1)

def play_talk(que):
    while 1:
        str = que.get()
        print("get file name = ", str)

        if (os.path.isfile(str)):
            pygame.mixer.music.load(str)
            pygame.mixer.music.play()
        else:
            print("file is no-exist")

def play_main():
    play_que = queue.Queue()

    # 创建线程
    thread_input = threading.Thread(target=play_input, args=(play_que,))
    thread_play = threading.Thread(target=play_talk, args = (play_que,))

    # 启动线程
    thread_play.start()
    thread_input.start()

if __name__ == '__main__':
    play_main()
