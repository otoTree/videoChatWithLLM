import cv2
import base64
import flet as ft
import time
import connect
from apiStore import *
import asr

chat = connect.Chat()


# 卡片组件
def card(role, content):
    if role == 'user':
        icon = 'ft.icons.BEACH_ACCESS'
    else:
        icon = 'ft.icons.ALBUM'
    c = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.ListTile(

                        leading=ft.Icon(eval(icon)),
                        title=ft.Text(role),
                        subtitle=ft.Text(content),
                    ),

                ],

            ),
            width=200,

            padding=10,
        )
    )

    return c


# 创建摄像头视频捕获对象
cap = cv2.VideoCapture(0)


def get_frame():
    global cap  # 因为我们在外部定义cap，所以需要使用global关键字

    # 读取一帧
    ret, frame = cap.read()

    # 确保帧能够被读取
    if ret:
        # 将捕获的帧转为JPEG格式。
        ret, jpeg = cv2.imencode('.jpg', frame)

        # 将JPEG格式的帧转为Base64
        base64_frame = base64.b64encode(jpeg)

        # 在Python3中，base64.b64encode()返回的是bytes类，如果需要字符串形式的base64，可以进行解码
        base64_frame = base64_frame.decode('utf-8')
    else:
        print("Couldn't capture frame")
        base64_frame = None  # 如果没有成功捕获帧，则将 base64_frame 设为 None。

    return base64_frame


video_control = 0


def main(page: ft.Page):
    def get_video():
        while True:
            # 获取一个新帧
            base64_frame = get_frame()

            # 如果成功获取了新帧
            if base64_frame:
                # 创建一个新的图片控件并将其添加到页面上
                img.src_base64 = base64_frame
                img.update()

            # 暂停1秒，然后继续获取下一个帧
            time.sleep(0.015)

    def send_click(e):
        lv.controls.append(card('user', new_message.value))

        page.update()

        chat.chat(get_frame(), new_message.value)

        print(chat.message)

        lv.controls.append(card(chat.message[-1]['role'], chat.message[-1]['content']))

        new_message.value = ""
        page.update()

    def close(e):
        global video_control
        video_control = 0
        print("关闭视频")
        page.remove(close_btn)

    def videoChat(e):
        global video_control
        video_control = 1
        page.add(close_btn)
        while True:
            if video_control == 0:
                break

            speech()#录音

            new_VoiceMessage = asr.main('00.wav') #语音识别

            lv.controls.append(card('user', new_VoiceMessage))

            if new_VoiceMessage == None:
                new_VoiceMessage=' '

            page.update()
            print(new_VoiceMessage)

            chat.chat(get_frame(), new_VoiceMessage)

            tts(chat.message[-1]['content']) #语音合成

            audio_playback('00.mp3')#播放语音

            lv.controls.append(card(chat.message[-1]['role'], chat.message[-1]['content']))
            page.update()

    base64_frame = get_frame()
    img = ft.Image(src_base64=base64_frame, width=300, height=300)

    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True, height=500)

    new_message = ft.TextField(hint_text="Please enter text here")
    new_message.border_color = '#3C3C3C'

    videoChat = ft.ElevatedButton("videoChat", on_click=videoChat)
    send = ft.ElevatedButton("Send", on_click=send_click)
    close_btn=ft.ElevatedButton("close", on_click=close)
    page.add(
        ft.Row(controls=[img, lv], alignment=ft.MainAxisAlignment.CENTER, ),
        ft.Row(controls=[videoChat,
                         new_message,
                         send],
               alignment=ft.MainAxisAlignment.CENTER, ),

    )
    get_video()


ft.app(target=main)

# 不要忘记在结束时释放摄像头资源
cap.release()
