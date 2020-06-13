# encoding:utf-8
import requests 
import urllib
import base64
import json
import matplotlib.pyplot as plt
from tkinter import *
import tkinter.filedialog

#第一步：选择待测图片
root = Tk()
path=tkinter.filedialog.askopenfilename()
root.destroy()

#第二步：获取access_token
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Ld3YPqMlO08wmFpHInwmEpi4&client_secret=X17n8XuxuUtxGUVWR1H9I4BsbQQ4SbYg'
response = requests.get(host)
if response:
   access_token=response.json()['access_token']
   
#第三步：将待测图片转为base64数据str格式
with open(path,"rb") as f:  
    base64_data = base64.b64encode(f.read())
    base64_data=base64_data.decode()

#第四步：上传图片数据，得出结果
request_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/classification/dogsss"
params = ("{\"image\":\""+base64_data+"\",\"top_num\":\"5\"}").encode(encoding='utf-8')
request_url = request_url + "?access_token=" + access_token
request = urllib.request.Request(url=request_url, data=params)
request.add_header('Content-Type', 'application/json')
response = urllib.request.urlopen(request)
content = response.read().decode()

#第五步：数据可视化，以便观察
if content:
    content=json.loads(content)
    sum=0
    for i in content['results']:
        sum+=i['score']
    result=[i['name'] for i in content['results']]
    score=[i['score'] for i in content['results']]
    result.append('others')
    score.append(1-sum)
    print(result)
    print(score)
    plt.pie(x=score,labels=result,explode=[0.1,0,0,0,0,0],shadow=True,autopct="%1.2f%%",radius=1)
    plt.legend(bbox_to_anchor=(0.8,-0.15),loc=3,borderaxespad=0)
    plt.title("results")
    plt.show()
