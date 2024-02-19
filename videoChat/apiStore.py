import speech_recognition as sr
import pygame
import os
import requests
import json
import base64
import uuid

def audio_playback(file_path):
    # 初始化 Pygame 库
    pygame.init()

    # 加载音乐文件
    pygame.mixer.music.load(file_path)

    # 获取音乐文件的长度，单位为秒
    audio_length = pygame.mixer.Sound(file_path).get_length()

    # 播放音乐
    pygame.mixer.music.play()

    # 循环检查音频是否已经播放完毕
    while pygame.mixer.music.get_busy():
        passed_time = pygame.mixer.music.get_pos() / 1000  # 毫秒转换为秒
        if passed_time >= audio_length:
            pygame.mixer.music.stop()  # 如果总时间已经过去，停止播放音乐

    # 关闭 Pygame 库
    pygame.quit()
    os.remove(file_path)


def speech():

    r = sr.Recognizer()
    # 启用麦克风
    mic = sr.Microphone()
    with mic as source:
        # 降噪
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    with open(f"00.wav", "wb") as f:
        # 将麦克风录到的声音保存为wav文件
        f.write(audio.get_wav_data(convert_rate=16000))

    return f"00.wav"





def tts(text):
    # 填写平台申请的appid, access_token以及cluster
    appid = "3430080075"
    access_token = "I3o5O7fiW-10KigZopBkUKjl8cTZdXdD"
    cluster = "volcano_tts"

    voice_type = "BV700_V2_streaming"
    host = "openspeech.bytedance.com"
    api_url = f"https://{host}/api/v1/tts"

    header = {"Authorization": f"Bearer;{access_token}"}

    request_json = {
        "app": {
            "appid": appid,
            "token": "access_token",
            "cluster": cluster
        },
        "user": {
            "uid": "388808087185088"
        },
        "audio": {
            "voice_type": voice_type,
            "encoding": "mp3",
            "speed_ratio": 1.0,
            "volume_ratio": 1.0,
            "pitch_ratio": 1.0,
        },
        "request": {
            "reqid": str(uuid.uuid4()),
            "text": text,
            "text_type": "plain",
            "operation": "query",
            "with_frontend": 1,
            "frontend_type": "unitTson"

        }
    }

    try:
        resp = requests.post(api_url, json.dumps(request_json), headers=header)
        print(f"resp body: \n{resp.json()}")
        if "data" in resp.json():
            data = resp.json()["data"]
            file_to_save = open("00.mp3", "wb")
            file_to_save.write(base64.b64decode(data))
    except Exception as e:
        e.with_traceback()

