import requests
import json
class Chat():
    def __init__(self):
        self.message=[]

    def connect(self,imgb64,query):
        # URL
        url = 'http://127.0.0.1:6006/'

        # 要发送的数据
        data = {
            'imgb64': imgb64,
            'query': query
        }

        # 发起POST请求
        response = requests.post(url, data=json.dumps(data))

        return response.text

    def chat(self,imgb64,query):
        try:

            self.message.append({'role': 'user', 'content': query})
            response=self.connect(imgb64,query)
            self.message.append({'role':'assistant','content':response})

            return response

        except:
            del self.message[-1]
            print('连接失败')
