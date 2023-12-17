from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import threading
import time

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

def wake_up():
    while True:
        print("执行唤醒任务...")
        # 在这里执行需要的唤醒操作
        # 比如请求自己的Flask应用以保持活跃

        # 每10分钟（600秒）执行一次
        time.sleep(600)

# 创建一个后台线程来执行唤醒任务
wake_up_thread = threading.Thread(target=wake_up)
wake_up_thread.daemon = True  # 设置为守护线程
wake_up_thread.start()

@app.route("/<path:path>", methods=['GET', 'POST', 'PUT', 'DELETE'])
def index(path):
    print(f'path={path}')
    headers = request.headers
    params = request.args

    # 对于 GET 请求，直接转发请求
    if request.method == 'GET':
        response = requests.get(path, params=params, headers={'Authorization': headers.get('Authorization')})
        print(f'response={response}')
        print(f'response.text={response.text}')
        return response.text, response.status_code

    # 对于 POST 和 PUT 请求，处理 JSON 数据
    if request.method in ['POST', 'PUT']:
        if request.content_type == 'application/json':
            json_data = request.json
            if request.method == 'POST':
                response = requests.post(path, json=json_data, headers=headers)
            else:  # PUT
                response = requests.put(path, json=json_data, headers=headers)
            return jsonify(response.json()), response.status_code
        else:
            # 返回错误消息或相应的响应
            return "Unsupported Media Type", 415


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
