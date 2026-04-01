import json
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 数据持久化文件路径
DATA_FILE = 'data.json'

def load_data():
    """
    从本地 JSON 文件读取数据。
    如果文件不存在，则初始化符合港大校园版前端需求的默认数据模型。
    """
    if not os.path.exists(DATA_FILE):
        # 初始默认数据：包含余额、宠物信息、语言偏好以及符合 Schema 的交易记录
        return {
            "balance": 8000.0,
            "petName": "Buddy",
            "currentPet": "tree",
            "language": "en",
            "transactions": [
                { 
                    "id": 1, 
                    "date": "2026-03-01", 
                    "item": "Monthly Allowance", 
                    "loc": "Bank", 
                    "cat": "Income", 
                    "amt": 8000.0, 
                    "type": "income" 
                },
                { 
                    "id": 2, 
                    "date": "2026-03-02", 
                    "item": "Hall Fee (Sassoon)", 
                    "loc": "Sassoon Rd", 
                    "cat": "Hall", 
                    "amt": 1800.0, 
                    "type": "expense" 
                }
            ]
        }
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # 如果文件损坏或读取失败，返回空的基础结构以防崩溃
        return {"balance": 0.0, "petName": "Pet", "currentPet": "tree", "language": "en", "transactions": []}

def save_data(data):
    """
    将数据以格式化的 JSON 形式保存到本地文件，确保跨会话持久化。
    """
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Error saving data: {e}")

@app.route('/')
def index():
    """渲染主页面 (templates/index.html)"""
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    """提供数据给前端，用于初始化页面状态"""
    return jsonify(load_data())

@app.route('/api/data', methods=['POST'])
def update_data():
    """
    接收并保存前端传回的完整状态。
    前端会在每次添加交易、更改宠物名或切换语言时调用此接口。
    """
    data = request.get_json()
    if data:
        save_data(data)
        return jsonify({"status": "success", "message": "Data saved successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid data received"}), 400

if __name__ == '__main__':
    # 启动 Flask 服务器。默认在 5000 端口运行。
    # 在开发模式下运行，代码修改后会自动重新加载。
    app.run(debug=True, port=5000)
