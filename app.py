from flask import Flask, request, jsonify
from chat import get_response
import json
import subprocess

app = Flask(__name__)

@app.route('/messages', methods=['POST'])
def receive_message():
    text = request.get_json().get("message")
    response = get_response(text)
    
    # Возвращаем ответ в формате JSON
    return jsonify({'response': response})

@app.route('/update_json', methods=['POST'])
def update_json():
    new_data = request.get_json()
    with open('intents.json', 'w', encoding='utf-8') as json_file:
        json.dump(new_data, json_file, ensure_ascii=False, indent=4)
    # Запускаем train.py асинхронно, чтобы не блокировать основной поток
    subprocess.run(['python', 'train.py'], shell=False)
    return jsonify({'response': 'JSON успешно обновлён и начат процесс обучения.'})

if __name__ == "__main__":
    app.run(debug=True, host='192.168.0.104', port=5000)
