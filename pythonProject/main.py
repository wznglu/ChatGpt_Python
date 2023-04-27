# -*- coding: utf-8 -*-
import openai
from flask import Flask, request, render_template, jsonify
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException


def clearchat(id):
    contentsDic[id].clear()
def chat(id,content):
    if id in contentsUser:
        print(f'您的请求太过频繁，请稍后再试..:{content}')
        return '您的请求太过频繁，请稍后再试..{}'.format(content)
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
            model="gpt-3.5-turbo-0301",
            max_tokens=maxreLenth,
            messages=mymessages
        )
        contentsDic[id].append({"role": "assistant", "content": rsp.choices[0].message.content})
        # print(json.dumps(rsp,ensure_ascii=False))
        # print(f'结果:{rsp},\n{rsp.choices[0].message.content}')
        print(f'结果:{rsp.choices[0].message.content}')
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
maxinputLenth=1800#最大提问字数
maxreLenth=1800#最大返回字数

contentsDic={}#玩家的聊天记录

contentsUser=[]#正在处理中的玩家，如果有再进来会有问题

contentIds=[]#微信会有会话id，会多次重试，得做写逻辑

#id,list[{"role": "", "content": ""}]


from flask import Flask
app = Flask(__name__)

@app.route('/chat', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        id=request.json['id']
        content=request.json['content']
        value = chat(id, content)
        value1={"id": id, "content": value}
        return jsonify(value1)
    else:
        global curID
        curID=curID+1
        return render_template('index.html',myid=curID)
    return value
# 用于验证微信服务器
@app.route('/wwxx', methods=['GET', 'POST'])
def wechat_auth():
    if request.method == 'GET':
        token = ''  # 替换为您的微信公众号设置的Token
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echo_str = request.args.get('echostr', '')

        try:
            check_signature(token, signature, timestamp, nonce)
        except InvalidSignatureException:
            return 'Invalid Signature'
        return echo_str
    elif request.method == 'POST':
        msg = parse_message(request.data)
        print(f'请求到来.:{msg}')
        if msg.id not in contentIds:
            contentIds.append(msg.id)
            if msg.type == 'text':
                value = chat(msg.source, msg.content)
                reply = create_reply('{}'.format(value), msg)
                contentIds.remove(msg.id)
                return reply.render()
            else:
                reply = create_reply('暂不支持该消息类型', msg)
                contentIds.remove(msg.id)
                return reply.render()
        else:
            reply = create_reply('waiting...',msg)
            return reply.render()
if __name__ == '__main__':
    openai.api_key =''#免费版
    #openai.api_key = ''#付费版
    #print(openai.Model.list())
    app.run(host='0.0.0.0',port=80)
