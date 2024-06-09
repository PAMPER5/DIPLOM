from flask import Flask, request, jsonify, send_file
from chat import get_response
import json
import subprocess

app = Flask(__name__)

@app.route('/messages', methods=['POST'])
def receive_message():
    text = request.get_json().get("message")
    response = get_response(text)
    
    return jsonify({'response': response})

@app.route('/update_json', methods=['POST'])
def update_json():
    new_data = request.get_json()
    with open('intents.json', 'w', encoding='utf-8') as json_file:
        json.dump(new_data, json_file, ensure_ascii=False, indent=4)
    subprocess.Popen(['python', 'train.py'], shell=False)
    return jsonify({'response': 'JSON успешно обновлён и начат процесс обучения.'})

@app.route('/get_questions', methods=['GET'])
def get_questions():
    file_path = 'questions.json'
    with open(file_path, 'r') as file:
        content = file.read()
    return content

if __name__ == "__main__":
    app.run(debug=True, host='192.168.0.106', port=5000)
