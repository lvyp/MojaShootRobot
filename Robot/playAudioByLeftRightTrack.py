#!/usr/bin/env python
# -*- coding: utf-8 -*-
import array
import sounddevice as sd
from pydub import AudioSegment


mapping_left_ch = 1  # 左声道为 1
mapping_right_ch = 2  # 右声道为 2
mapping_stereo = None  # 立体声为 None


def trans_mp3_to_wav(filepath):
    song = AudioSegment.from_mp3(filepath)
    fileName = filepath.replace("mp3", "wav")
    song.export(fileName, format="wav")
    return fileName


class MyException(Exception):
    """
    自定义的异常类
    """
    def __init__(self, *args):
        self.args = args


def play_audio_file(audio_file_path, channel_id, sample_rate, mapping_ch):

    # 将本机默认的输出声道, 改为 自己设定的声道
    # sd.default.device 是一个列表, 第一个元素是: 默认的输入设备id;    第二个是默认的输出设备id
    sd.default.device[1] = channel_id

    # 常选参数, 一个数据, 一个采样率, 另外还有一个: blocking=True, 若设置, 则表示播放完毕当前音频再往下进行程序
    #data_array = read_data(audio_file_path, audio_channels)
    data_array = array.array('h')
    with open(audio_file_path, 'rb') as fh:
        data_array.frombytes(fh.read())

    #可以通过直接设置形参block的值进行阻塞
    sd.play(data_array, blocking=True, samplerate=sample_rate, mapping=mapping_ch)
    #sd.wait()  # 表示等到此音频文件播放完毕之后再往下进行程序
    #time.sleep(20)  # 使用 time.sleep() ---> 休眠几秒, 音频文件就播放几秒, 时长自己控制

    # 注: 如果没有 类似休眠 等延时操作, 则程序只会一闪而过, 不会播放音频


def get_audio_devices_all_msg_dict(rec_file_path, speakerName):
    audio_drivers_and_channels_msg_dict = {}
    audio_input_channels_msg_dict = {}
    audio_output_channels_msg_dict = {}

    # 使用sounddevice 获取电脑连接的声卡以及系统自带的所有音频驱动信息(驱动, 声道名, id)
    this_tmp_dict = {}
    host_api_tuple = sd.query_hostapis()

    for temp_dict in host_api_tuple:
        this_tmp_dict[temp_dict["name"]] = temp_dict["devices"]

    channels_list = sd.query_devices()
    for driver_name in this_tmp_dict:
        audio_drivers_and_channels_msg_dict[driver_name] = []
        audio_input_channels_msg_dict[driver_name] = []
        audio_output_channels_msg_dict[driver_name] = []

        for deviceId in this_tmp_dict[driver_name]:
            audio_drivers_and_channels_msg_dict[driver_name].append((deviceId, channels_list[deviceId]["name"]))

    # print(audio_drivers_and_channels_msg_dict)
    mapping_ch = mapping_stereo
    if speakerName == "小竹":
        mapping_ch = mapping_left_ch
    elif speakerName == "老竹":
        mapping_ch = mapping_right_ch
    else:
        pass
    for device in audio_drivers_and_channels_msg_dict['Windows DirectSound']:
        if device[1] == '耳机 (High Definition Audio Device)':
            play_audio_file(rec_file_path, device[0], 16000, mapping_ch)
        elif device[1] == '扬声器 (Realtek High Definition Audio)':
            play_audio_file(rec_file_path, device[0], 16000, mapping_ch)
        elif device[1] == 'Headphones (High Definition Audio Device)':
            play_audio_file(rec_file_path, device[0], 16000, mapping_ch)


if __name__ == "__main__":
    rec_file_path = "./tts/2.wav"
    #rec_file_path = trans_mp3_to_wav(rec_file_path)
    get_audio_devices_all_msg_dict(rec_file_path, "小竹")
    get_audio_devices_all_msg_dict(rec_file_path, "老竹")
