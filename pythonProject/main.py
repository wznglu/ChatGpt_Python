# This is a sample Python script.
import json
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import time

import openai
from flask import Flask, request, render_template, jsonify


# import ssl
# ssl.match_hostname = lambda cert, hostname: True
def inputchat():
    content=input("输入您的问题\n")
    #contents.append(content)
    value = chat("1",content)
    #contents.append(value.choices[0].message.content)
    # print(value)
    inputchat()

def clearchat(id):
    contentsDic[id].clear()
def chat(id,content):
    if id in contentsUser:
        return "您的请求太过频繁，请稍后再试..."
    contentsUser.append(id)
    q = content
    if id in contentsDic.keys():
        contentsDic[id].append({"role": "user", "content": q})
    else:
        contentsDic[id]=[]
        contentsDic[id].append({"role": "user", "content": q})

    if len(contentsDic[id])>maxchatCount:#移除一条提问与一条回答 保留第0条system设定
        contentsDic[id].remove(contentsDic[id][1])
        contentsDic[id].remove(contentsDic[id][1])

    value=contentsDic[id]
    count = len(value) - maxcontentCount
    if  count<0:
        count=0
    elif count % 2 == 1:#保证从提问开始
        count=count+1

    mymessages = []
   # mymessages.append({"role": "system", "content": ""})  # 初始化
    value1=value[count:]
    value1.reverse()
    i=0
    lenth=0
    for site in value1:
        # site1=eval(site)
        lenth=lenth+len(site["content"])
        mymessages.append(site)
        if lenth>maxinputLenth:
            if  i%2==1:
                mymessages.pop()
            else:
                mymessages.pop()
                mymessages.pop()
            break
        i = i + 1
    mymessages.append({"role": "system", "content": ""})  # 初始化
    mymessages.reverse()

    print(f'提问参数,id:{id}, content: {mymessages}')

    try:
        rsp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=maxreLenth,
            messages=mymessages
        )
        contentsDic[id].append({"role": "assistant", "content": rsp.choices[0].message.content})
        # print(json.dumps(rsp,ensure_ascii=False))
        contentsUser.remove(id)
        return rsp.choices[0].message.content
    except Exception as e:
        print('发生了异常：',e)
        contentsUser.remove(id)
        return "error"
    finally:
        pass
   # inputchat()

curID=0#测试目前自己管理id

maxchatCount=100#最大保留聊天记录条数
maxcontentCount=10#上下文条数
maxinputLenth=2048#最大提问字数
maxreLenth=2048#最大返回字数

contentsDic={}

contentsUser=[]

#id,list[{"role": "", "content": ""}]


from flask import Flask
app = Flask(__name__)

@app.route('/chat', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        # id=request.form['id']
        # content=request.form['content']
        id=request.json['id']
        content=request.json['content']
        value = chat(id, content)
        value1={"id": id, "content": value}
        return jsonify(value1)
        # return render_template('index.html', result=value1)
    else:
        global curID
        curID=curID+1
        #id = request.args['id']
        #content = request.args['content']
        return render_template('index.html',myid=curID)

    return value
if __name__ == '__main__':
    openai.api_key = ''  # os.getenv("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")
    app.run(host='192.168.124.26',port=5000)


# if __name__ == '__main__':
#     print('PyCharm')
#     openai.api_key = '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'#  os.getenv("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")
#     # print(openai.Model.list())
#     #inputchat()