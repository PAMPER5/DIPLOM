from flask import Flask, request, jsonify, send_from_directory
from chat import get_response
import json
import subprocess
import os

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
    subprocess.Popen(['python', 'train.py'], shell=False)
    return jsonify({'response': 'JSON успешно обновлён и начат процесс обучения.'})

@app.route('/get_questions', methods=['GET'])
def get_questions():
    # Убедитесь, что путь к файлу безопасен
    if os.path.exists('questions.json'):
        return send_from_directory(directory='.', path='questions.json', as_attachment=True)
    else:
        return jsonify({'response': 'Файл questions.json не найден.'})

if __name__ == "__main__":
    app.run(debug=True, host='192.168.0.106', port=5000)
