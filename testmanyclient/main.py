# This is a sample Python script.
import json
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

import requests as requests


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def post_request(id):

        payload = {'id': id, 'content': '你好'}  # 要发送的POST数据
        url = 'http://192.168.124.26:5000/chat'
        response = requests.post(url, json=payload)

        response_json = json.loads(response.text)
        # print(response_json['content'])  # 输出响应内容
        return response_json['content']
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    ids = ['1', '2', '3','4']



    with mp.Pool(processes=4) as pool:
        # results = pool.map(post_request, [url] * 4,ids)
        results = pool.map(post_request, ids)
        # 输出所有响应内容
    for result in results:
        print(result)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
