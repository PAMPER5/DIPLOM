from flask import Flask, request, jsonify
from chat import get_response
import json

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
        # Установка ensure_ascii=False для сохранения символов в их исходном виде
        json.dump(new_data, json_file, ensure_ascii=False, indent=4)
    return jsonify({'response': 'JSON успешно обновлён.'})

if __name__ == "__main__":
    app.run(debug=True, host='192.168.0.104', port=5000)
