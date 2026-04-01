import json
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 数据持久化文件
DATA_FILE = 'data.json'

def load_data():
    """从本地 JSON 文件读取数据"""
    if not os.path.exists(DATA_FILE):
        # 初始默认数据
        return {
            "balance": 5000.0,
            "petName": "Buddy",
            "currentPet": "tree",
            "language": "en",
            "transactions": [
                { "id": 1, "date": "2026-03-01", "item": "Initial Balance", "loc": "Bank", "cat": "Income", "amt": 5000, "type": "income" }
            ]
        }
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    """保存数据到本地"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(load_data())

@app.route('/api/data', methods=['POST'])
def update_data():
    save_data(request.json)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    # 运行此文件启动服务器
    app.run(debug=True, port=5000)
