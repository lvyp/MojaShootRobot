# -*- coding: utf-8 -*-
# @Time : 2021/6/11 10:12
# @Author :
# @Site : Beijing
# @File : speechRecognitionMode.py
# @Software: PyCharm

import ctypes
import threading
import os
import win32api
import globalVariable
from loggerMode import logger
from ctypes import *
import random
import pyaudio
import wave
from playsound import playsound
import BaiduCloudClass
import playAudioByLeftRightTrack as LRTrack
from tuning import Tuning
import usb
import time


RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 1  # change base on firmwares, default_firmware.bin as 1 or i6_firmware.bin as 6
RESPEAKER_WIDTH = 2
# run getDeviceInfo.py to get index
RESPEAKER_INDEX = 1  # refer to input device id
CHUNK = 1024
RECORD_SECONDS = 4
WAVE_OUTPUT_FILENAME = "./MicRecording/output.wav"
WAKEUP_RESPONSE_PATH = "./TtsRecording/wakeUpResponse/"
TTS_BY_BAIDUCLOUD_PATH = "./TtsRecording/BaiduCloud/TtsResponse.mp3"
TTS_BY_EXCEPTION_PATH = "./TtsRecording/Exception/"
TTS_BY_NOTGETVOICE_PATH = "./TtsRecording/NotGetVoice/"


def PlayVoice(path):
    # print(path)
    playJudge = playsound(path, True)  # 设置为True需要同步进行。否则录音时会将播放的应该回复录入
    if playJudge is False:
        logger.info("音频格式不正确，无法播放！！\n")
    else:
        logger.info("对话应答已回复！！\n")


def NotGetVoiceResponse():
    # 获取没有语音输入文件夹内所有文件名称，进行随机答复
    wakeUpWordlist = os.listdir(TTS_BY_NOTGETVOICE_PATH)
    fileNameStr = random.sample(wakeUpWordlist, 1)
    logger.info("异常音频为" + fileNameStr[0])
    PlayVoice(TTS_BY_NOTGETVOICE_PATH + fileNameStr[0])


def ExceptionResponse():
    # 获取异常文件夹内所有异常文件名称,进行随机答复
    wakeUpWordlist = os.listdir(TTS_BY_EXCEPTION_PATH)
    fileNameStr = random.sample(wakeUpWordlist, 1)
    logger.info("异常音频为" + fileNameStr[0])
    PlayVoice(TTS_BY_EXCEPTION_PATH + fileNameStr[0])


def wakeUpResponse():
    # 获取唤醒词文件夹内所有唤醒词名称,进行随机答复
    wakeUpWordlist = os.listdir(WAKEUP_RESPONSE_PATH)
    if len(wakeUpWordlist) == 0:
        logger.info("没有唤醒应答文件唤醒！！答复失败！！\n")
    else:
        fileNameStr = random.sample(wakeUpWordlist, 1)
        logger.info("唤醒词音频为" + fileNameStr[0])
        PlayVoice(WAKEUP_RESPONSE_PATH + fileNameStr[0])


def micGenerateRocord():

    mojaMic = pyaudio.PyAudio()
    micInfo = mojaMic.get_host_api_info_by_index(0)
    numdevices = micInfo.get('deviceCount')
    for i in range(0, numdevices):
        if (mojaMic.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            pass
            # logger.info("Input Device id " + str(i) + " - " + str(mojaMic.get_device_info_by_host_api_device_index(0, i).get('name').encode("GBK", "ignore")))
            # print("Input Device id ", i, " - ", mojaMic.get_device_info_by_host_api_device_index(0, i).get('name'))
    # 开始录音
    stream = mojaMic.open(
        rate=RESPEAKER_RATE,
        format=mojaMic.get_format_from_width(RESPEAKER_WIDTH),
        channels=RESPEAKER_CHANNELS,
        input=True,
        input_device_index=RESPEAKER_INDEX, )
    logger.info("* recording")

    frames = []

    for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    logger.info("* done recording")

    stream.stop_stream()
    stream.close()
    mojaMic.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(RESPEAKER_CHANNELS)
    wf.setsampwidth(mojaMic.get_sample_size(mojaMic.get_format_from_width(RESPEAKER_WIDTH)))
    wf.setframerate(RESPEAKER_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


# 声源定位
def voiceDirection():
    dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
    dev.set_configuration()

    if dev and (globalVariable.moveStatus == 0):
        Mic_tuning = Tuning(dev)
        print("位置信息: " + str(Mic_tuning.direction))
        # 控制底盘转动角度


def commandSend(intent, slots):
    # 当指令为机器人导览并且机器人未运动时，会执行导览命令
    if (intent == "ROBOT_GUIDE") and (globalVariable.moveStatus == 0):
        # globalVariable.set_position_name()  # web API使用
        globalVariable.set_position_name_by_serial(globalVariable.mojaSerial.get_target_list())
        globalVariable.set_value("mapRouteSettingFlag", True)
    else:
        pass


def speechRecognitionMode():
    # 语音识别模块:
    # 1.判断是否是唤醒词（科大讯飞SDK）
    # 2.唤醒后获取麦克风数据生成音频文件
    # 3.将音频文件推送到百度云，获取ASR、NLU以及TTS音频
    # 4.播放TTS音频并解析NLU，根据相应的意图与槽值发送指令给相应模块
    logger.info("语音识别模块入口")
    event = globalVariable.get_event()
    rLock = threading.RLock()
    while 1:
        rLock.acquire()
        # logger.info("线程：" + threading.current_thread().name + " Id:" + str(threading.get_ident()))
        # 判断是否被唤醒
        cppDll = CDLL("awaken_sample")
        cppDll.CFunction.restype = ctypes.c_uint64  # 修改lib.bar返回类型
        returnValue = str(cppDll.CFunction())
        win32api.FreeLibrary(cppDll._handle)  # 释放DLL资源，防止DLL变量未释放影响再次唤醒动作
        if returnValue == "202":
            logger.info("唤醒成功！！\n")
            # 声源定位
            voiceDirection()
            # 播放音频回复用户
            wakeUpResponse()
            # 进行麦克风收音，生成音频文件
            # micGenerateRocord()
            # 将音频发送给百度云进行ASR解析
            baiDuCloud = BaiduCloudClass.BaiduCloud()
            # mojaAsr = baiDuCloud.call_asr(WAVE_OUTPUT_FILENAME)
            mojaAsr = baiDuCloud.ASR()
            logger.info("mojaAsr:" + mojaAsr)
            if mojaAsr == "Exception Happened":
                ExceptionResponse()
            elif mojaAsr == "":
                NotGetVoiceResponse()
            else:
                # 将ASR识别结果发送给NLU进行自然语言处理
                mojaNlu = BaiduCloudClass.Baidu_NLU()
                answer = mojaNlu.get_NLU(mojaAsr)
                # logger.info("answer:" + str(answer))
                if "error" in answer.keys():
                    ExceptionResponse()
                else:
                    intent = answer["schema"]["intent"]
                    slots = answer["schema"]["slots"]
                    logger.info("intent: " + str(intent) + "\nslots: " + str(slots))
                    mojaTts = baiDuCloud.call_tts(answer["action_list"][0]["say"])
                    if mojaTts == "Successful":
                        TTS_WAV = LRTrack.trans_mp3_to_wav(TTS_BY_BAIDUCLOUD_PATH)
                        LRTrack.get_audio_devices_all_msg_dict(TTS_WAV, "小竹")
                        # PlayVoice(TTS_BY_BAIDUCLOUD_PATH)
                    else:
                        ExceptionResponse()
                    # 根据NLU返回的intent和slot进行判断控制相应的线程
                    commandSend(intent, slots)
        elif returnValue == "201":
            logger.info("登录失败！！\n")
        elif returnValue == "200":
            logger.info("没有唤醒！！\n")
        # globalVariable.set_value("actionFlag", True)
        event.set()
        rLock.release()
