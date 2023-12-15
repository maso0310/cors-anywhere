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
    headers = request.headers
    params = request.args
    json_data = request.json
    form_data = request.form.to_dict()
    if request.method == 'GET':
        response = requests.get(path, params=params, headers={'Authorization': headers.get('Authorization')})
        print(f'jsonify(response.json())={jsonify(response.json())}')
        print(f'response.status_code={response.status_code}')
        return jsonify(response.json()), response.status_code
    elif request.method == 'POST':
        response = requests.post(path, data=form_data, json=json_data, headers=headers)
        return jsonify(response.json()), response.status_code
    elif request.method == 'PUT':
        response = requests.put(path, data=form_data, json=json_data, headers=headers)
        return jsonify(response.json()), response.status_code
    return path


if __name__ == "__main__":
    app.run(debug=True, port=1234)
