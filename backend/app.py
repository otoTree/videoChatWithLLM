import torch
from modelscope import snapshot_download
import os
from modelscope import AutoTokenizer, AutoModelForCausalLM
import base64
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
#若模型存在则读取，否则下载
model_dir = snapshot_download('Shanghai_AI_Laboratory/internlm-xcomposer2-vl-7b', cache_dir='model', revision='master')

#指定工作显卡
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

#模型导入
tokenizer = AutoTokenizer.from_pretrained(model_dir, revision='master', trust_remote_code=True)
# `torch_dtype=torch.float16` 可以令模型以 float16 精度加载，否则 transformers 会将模型加载为 float32，导致显存不足
model = AutoModelForCausalLM.from_pretrained(model_dir, revision='master', 
                        torch_dtype=torch.float32, trust_remote_code=True,device_map="auto")
model = model.eval()
from modelscope import snapshot_download
# self.vision_tower_name = snapshot_download("AI-ModelScope/clip-vit-large-patch14-336")
model.tokenizer = tokenizer


history=[]

#聊天和LLM
def chat(text):
    global history
    image = '0.png'
    query = '<ImageHere>'+text
    print(query)
    response, history = model.chat(query=query, image=image, tokenizer= tokenizer,history=[])
    return response

#b64解码
def decode(imgb64):
    # Base64编码的图片数据的字符串
    b64_string = imgb64

    # 对字符串进行解码
    image_data = base64.b64decode(b64_string)

    # 将字节数据转换为图像
    image = Image.open(BytesIO(image_data))

    # 保存图像到文件系统
    image.save('0.png')

#后端
app = FastAPI()

# 创建一个用于接收数据的 Pydantic 模型
class Data(BaseModel):
    imgb64: str
    query: str = None

# 定义 POST 路径操作
@app.post("/")
async def LLM(item: Data):
    decode(item.imgb64)
    response=chat(item.query)
    return response



